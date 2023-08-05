try:
    import cPickle as pickle
except:
    import pickle
from os.path import expanduser, join, split
from os import remove, makedirs, rename
from glob import glob
import atexit
import zlib


class Link(object):
    """
    This abstract base class provides shared functionality for any hard disk linked
    class required. The other classes in this library use this class, and can be
    referred to if you need to implement your own version. (Please consider a pull
    request at https://github.com/cdusold/DriveLink if you make a good general
    implementation.)

    .. attention:: All classes in DriveLink use this class, so the following applies
                   to each of them.

    To be able to implement your own, in addition to implementing the abstract functions,
    you have to implement self.pages as a dictionary that will work for your class.

    This base class provides wrapping that automatically saves to disk, if everything
    is implemented correctly in inheriting classes. It provides the ability to access
    implementing classes directly (direct use of Class.close() reccommended) or
    through a context manager.

    .. note:: This abstract class is not thread safe, nor is it process safe. Any multithreaded
              or multiprocessed uses of implemented classes hold no guarantees of accuracy.

    You can configure how this class stores things in a few ways.

    The file_basename parameter allows you to keep multiple different stored objects
    in the same file_location, which defaults to .DriveLink in the user's home folder.
    Using a file_basename of the empty string may cause a small slowdown if more
    than just this object's files are in the folder. Using substrings of other basenames
    or basenames that end in numbers may cause irregular behavior. Using a file_location
    of the empty string will result in files being placed in the environment's current
    location (i.e. what `os.getcwd()` would return).

    The size_limit parameter determines how many items are kept in each page, and the
    max_pages parameter determines how many pages can be kept in memory at the same
    time. If you use smaller items in the class, increasing either is probably a
    good idea to get better performance. This setting will only use about 128 MB if
    standard floats or int32 values. Likely less than 200 MB will ever be in memory,
    which prevents the RAM from filling up and needing to use swap space. Tuning
    these values will be project, hardware and usage specific to get the best results.
    Even with the somewhat low defaults, this will beat out relying on python to
    use swap space.

    In order to speed up disk access, you can specify a compression_ratio. compression
    is performed using Python's built in `ZLib library <https://docs.python.org/library/zlib.html>`_.
    """

    def __init__(self, file_basename, size_limit=1024, max_pages=16, file_location=join(expanduser("~"), ".DriveLink"), compression_ratio=0):
        if max_pages < 1:
            raise ValueError("There must be allowed at least one page in RAM.")
        self.max_pages = max_pages
        if size_limit < 1:
            raise ValueError("There must be allowed at least one item per page.")
        self.size_limit = size_limit
        if file_location:
            try:
                makedirs(file_location)
            except OSError as e:
                if e.errno != 17:
                    raise
                pass
        self._file_base = join(file_location, file_basename)
        self._file_loc = file_location
        self._file_basename = file_basename
        self._compression = compression_ratio
        self._length = 0
        self._queue = []
        # Just in case, cache pickle.
        self._pickle = pickle
        self._check_old_settings()
        self.load_index()
        atexit.register(Link.close, self)

    def _check_old_settings(self):
        """
        This loads and saves the settings used to create the drivelink. If different
        settings were used originally, this may conflict with the operation of the
        link, so the values will be copied out into the new structure.
        """
        try:
            with open(self._file_base + 'Set', 'rb') as f:
                size_limit = self._pickle.load(f)
            if size_limit != self.size_limit:
                self._make_old_values_available(size_limit)
        except IOError:
            pass
        with open(self._file_base + 'Set', 'wb') as f:
             self._pickle.dump(self.size_limit, f)

    def _make_old_values_available(self, size_limit):
        """
        In order to take advantage of lazy loading, it may be worth your time to
        overload this function when you inherit and implement a recovery method yourself.

        You have to implement the copy_from function to be able to use this anyway.
        """
        for file_name in glob(self._file_base+"*"):
            path, name = split(file_name)
            rename(file_name, join(path, "~"+name))
        with type(self)(self._file_base, self.size_limit, min(4, self.max_pages), self._file_loc) as new:
            with type(self)("~"+self._file_basename, size_limit, 1, self._file_loc, -1) as old:
                new.copy_from(old)
        for file_name in glob(join(self._file_loc, "~"+self._file_basename+"*")):
            remove(file_name)

    def copy_from(self, other):
        """
        Depending on the type of container this link is wrapping, this will transfer
        values from a container of the same time to the new one.
        """
        raise NotImplementedError

    _stored_index = None
    def load_index(self):
        """
        This base implementation loads the number of entries in the collection and
        returns anything else that may be stored with it. If the inheriting class
        requires more than just a length value to index its items, it is reccommended
        to override this method and store_index, so that loading is automatic.
        """
        try:
            with open(self._file_base + 'Len', 'rb') as f:
                self._stored_index = f.read()
                other_values = self._pickle.loads(self._stored_index)
                other_values, self._length = other_values[:-1], other_values[-1]
        except IOError:
            return None
        return other_values

    def store_index(self, *other_values):
        """
        This base implementation saves the number of entries in the collection and
        anything passed into the function with it. If the inheriting class
        requires more than just a length value to index its items, it is reccommended
        to override this method and load_index, so that loading is automatic.

        To save additional items, just pass them as arguments to a super call.
        """
        to_save = self._pickle.dumps(tuple(other_values) + (self._length,))
        if to_save == self._stored_index:
            return
        with open(self._file_base + 'Len', 'wb') as f:
            f.write(to_save)
        self._stored_index = to_save

    def __len__(self):
        '''
        Returns the number of entries stored.
        '''
        return self._length

    def __repr__(self):
        return (self.__class__.__name__ + "('" + self._file_basename + "', " +
                str(self.size_limit) + ', ' + str(self.max_pages) + ", '" + self._file_loc + "')")

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_val, trace):
        self.close()
        del self

    def close(self):
        '''
        Save all the values to disk before closing.
        '''
        if (self is None or not hasattr(self, "_save_page_to_disk")
                or not hasattr(self, "_file_base") or self._file_base is None):
            return
        while len(self.pages) > 0:
            for key in set(self.pages.keys()):
                self._save_page_to_disk(key)

    def _guarantee_page(self, k):
        """
        Ensures the page is available.
        """
        if k not in self.pages:
            self.open_page(k)
        while len(self._queue) > self.max_pages:
            if self._queue[0] == k:
                self._queue.append(self._queue[0])
                del self._queue[0]
            self._save_page_to_disk(self._queue[0])

    def open_page(self, k):
        """
        Once it is determined a page isn't in RAM, make it so.

        This will load a page if it is saved to disk, or create a new one when necessary.
        """
        raise NotImplementedError

    def _finditem(self, key):
        """
        Pulls up the page containing the key in question.
        """
        k, i = self.determine_index(key)
        self._guarantee_page(k)
        return k, i

    def determine_index(self, key):
        """
        Figures out where the key in question should be.
        """
        raise NotImplementedError

    def __setitem__(self, key, value):
        '''
         Sets a value that a key maps to.
        '''
        i, k = self._finditem(key)
        if k not in self.pages[i]:
            # If this isn't possible, the implemented page should throw an error.
            self.pages[i][k] = value
            self._length += 1
        else:
            self.pages[i][k] = value

    def __getitem__(self, key):
        '''
         Retrieves the value the key maps to.
        '''
        i, k = self._finditem(key)
        return self.pages[i][k]

    def __delitem__(self, key):
        '''
         Deletes the entry in question from the pages.
        '''
        i, k = self._finditem(key)
        del self.pages[i][k]
        self._length -= 1

    def __contains__(self, item):
        for page in self._iterpages():
            if item in page:
                return True
        return False

    def _iterpages(self):
        """
        Pulls up page after page and cycles through all of them.
        """
        for k in self.page_indices():
            self._guarantee_page(k)
            yield self.pages[k]

    def __iter__(self):
        '''
         Iterates through all the keys stored.
        '''
        for p in self._iterpages():
            for i in p:
                yield i

    def page_indices(self):
        """
        Yields an iterable containing each page.
        """
        raise NotImplementedError

    def _save_page_to_disk(self, number):
        self.store_index()
        if self._file_base:
            if number in self.pages:
                if len(self.pages[number]) > 0:
                    to_save = self._pickle.dumps(self.pages[number])
                    if self._compression:
                        to_save = zlib.compress(to_save, self._compression)
                    with open(self._file_base + str(number), 'wb') as f:
                        f.write(to_save)
                else:
                    self.page_removed(number)
                del self.pages[number]
            for i in range(len(self._queue)):
                if self._queue[i] == number:
                    del self._queue[i]
                    break

    def _load_page_from_disk(self, number):
        if self._file_base:
            with open(self._file_base + str(number), 'rb') as f:
                to_load = f.read()
            try:
                to_load = zlib.decompress(to_load)
            except zlib.error:
                pass
            self.pages[number] = self._pickle.loads(to_load)
            self._queue.append(number)
            remove(self._file_base + str(number))
