import io
import os
import queue
import hashlib
import logging
import threading

import steov

class FileHouse:
    _block_size = 4096

    def __init__ (self, root):
        self._root = root
        self._temp_file = os.path.join(self._root, "temp")
        if os.path.exists(self._temp_file):
            os.remove(self._temp_file)
        self._logger = logging.getLogger(__name__)

    def persist (self, blob):
        if blob is None:
            return None
        blob_id = hashlib.sha256(blob).hexdigest()
        self._queue.put((blob_id, blob))
        return blob_id

    def start (self):
        self._is_aborted = False
        self._queue = queue.Queue()
        self._thread = threading.Thread(target=self._run)
        self._thread.start()

    def stop (self):
        self._queue.put(None)
        self._thread.join()

    def abort (self):
        self._is_aborted = True
        self.stop()
        while self._queue.qsize():
            self._queue.get()
            self._queue.task_done()

    def __enter__ (self):
        self.start()
        return self

    def __exit__ (self, type, value, traceback):
        self.stop()



    def _run (self):
        while not self._is_aborted:
            blob_id = None
            item = self._queue.get()
            try:
                if item is None:
                    break
                blob_id, blob = item
                prefix1 = blob_id[:2]
                prefix2 = blob_id[2:4]
                suffix = blob_id[4:]
                blob_dir = os.path.join(self._root, prefix1, prefix2)
                blob_file = os.path.join(blob_dir, suffix)
                if os.path.exists(blob_file):
                    continue
                os.makedirs(blob_dir, exist_ok=True)
                with io.BytesIO(blob) as blob_stream:
                    with open(self._temp_file, "wb") as fp:
                        while not self._is_aborted:
                            block = blob_stream.read(self._block_size)
                            if not block:
                                break
                            fp.write(block)
                os.rename(self._temp_file, blob_file)
            except Exception as ex:
                self._logger.error("filehouse.run.stacktrace: " + repr(steov.format_exc()))
                self._logger.error("filehouse.run.blob_id: " + repr(blob_id))
            finally:
                self._queue.task_done()
