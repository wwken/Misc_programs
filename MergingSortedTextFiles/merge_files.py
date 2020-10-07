import sys
import os
import heapq


class FileReader(object):
    def __init__(self, input_file_location):
        self.fh = open(input_file_location, "rt")

    def next_line(self):
        line = self.fh.readline()
        if line:
            return line
        else:
            self.fh.close()
            return None


class FileWriter(object):
    def __init__(self, output_file):
        self.fh = open(output_file, "wt")

    def write_line(self, line):
        self.fh.write(line)

    def close(self):
        self.fh.close()


class MergeFilesHelper(object):
    def __init__(self, input_files, output_merge_file_location):
        self.all_file_readers = [
            {
                'previous_line': None,
                'file_reader': FileReader(f),
                'file_location': f
            }
            for f in input_files
        ]
        self.file_writer = FileWriter(output_merge_file_location)
        self.heap_max_size = len(input_files)
        self.li = []
        self.heap_count = 0
        heapq.heapify(self.li)

    def _store_line(self, line):
        heapq.heappush(self.li, line)
        self.heap_count += 1
        if self.heap_count > self.heap_max_size:
            self.file_writer.write_line(heapq.heappop(self.li))
            self.heap_count -= 1

    def execute(self):
        li = []
        while True:
            at_least_one_read = False
            for file_reader in self.all_file_readers:
                if not file_reader['file_reader']:
                    continue
                this_line = file_reader['file_reader'].next_line()
                at_least_one_read = True
                if this_line:   # if there is input line
                    if this_line == '\n':
                        continue
                    if file_reader['previous_line'] and this_line < file_reader['previous_line']:
                        raise ValueError(f"Input file: {file_reader['file_location']} is not sorted lexicographically"
                                         f" at line: {this_line} vs the previous line: {file_reader['previous_line']}")
                    self._store_line(this_line)
                    file_reader['previous_line'] = this_line    # now storing this line as previous and go for next
                else:
                    file_reader['file_reader'] = None
            if not at_least_one_read:
                break
        # print("Done, closing the file...")
        # now pop all items in the heap and write to the file
        while self.heap_count > 0:
            self.file_writer.write_line(heapq.heappop(self.li))
            self.heap_count -= 1

        self.file_writer.close()


def get_files_from_dir(dir_path):
    files = os.listdir(dir_path)
    return files


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Number of arguments wrong! Please run the program in this manner: ./merge_files input_dir output.dat")

    input_dir = sys.argv[1]
    output_merge_file_location = sys.argv[2]

    input_files = [os.path.join(input_dir, f) for f in get_files_from_dir(input_dir)]
    merge_file_helper = MergeFilesHelper(input_files, output_merge_file_location)
    merge_file_helper.execute()

