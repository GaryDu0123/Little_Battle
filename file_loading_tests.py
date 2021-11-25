from little_battle import load_config_file
import unittest

# Don't remove any comments in this file
folder_path = "invalid_files/"


# Please create appropriate invalid files in the folder "invalid_files"
# for each unit test according to the comments below and
# then complete them according to the function name

class Test(unittest.TestCase):

    def test_file_not_found(self):
        # no need to create a file for FileNotFound
        try:
            load_config_file(f"{folder_path}/file")
        except FileNotFoundError:
            print("FileNotFoundError Pass")
        except Exception as e:
            print(e)
            assert not e, "FAIL Test FileNotFound"
        else:
            assert False, "FAIL Test FileNotFound"

    def test_format_error(self):
        # add "format_error_file.txt" in "invalid_files"
        try:
            load_config_file(f"{folder_path}/format_error_file.txt")
        except SyntaxError as e:
            assert str(e) == "Invalid Configuration File: format error!", "FAIL Test format_error"
            print("format_error Pass")
        except Exception as e:
            print(e)
            assert not e, "FAIL Test format_error"
        else:
            assert False, "FAIL Test format_error"

    def test_frame_format_error(self):
        # add "frame_format_error_file.txt" in "invalid_files"
        try:
            load_config_file(f"{folder_path}/frame_format_error_file.txt")
        except SyntaxError as e:
            assert str(e) == "Invalid Configuration File: frame should be in format widthxheight!", "FAIL Test frame_format_error"
            print("format_error Pass")
        except Exception as e:
            print(e)
            assert not e, "FAIL Test frame_format_error"
        else:
            assert False, "FAIL Test frame_format_error"

    def test_frame_out_of_range(self):
        # add "format_out_of_range_file.txt" in "invalid_files"
        try:
            load_config_file(f"{folder_path}/format_out_of_range_file.txt")
        except ArithmeticError as e:
            assert str(e) == "Invalid Configuration File: width and height should range from 5 to 7!", "FAIL Test format_out_of_range"
            print("format_out_of_range Pass")
        except Exception as e:
            print(e)
            assert not e, "FAIL Test format_out_of_range"
        else:
            assert False, "FAIL Test format_out_of_range"

    def test_non_integer(self):
        # add "non_integer_file.txt" in "invalid_files"
        try:
            load_config_file(f"{folder_path}/non_integer_file.txt")
        except ValueError as e:
            assert str(e) == "Invalid Configuration File: Wood contains non integer characters!", "FAIL Test non_integer_file"
            print("non_integer_file Pass")
        except Exception as e:
            print(e)
            assert not e, "FAIL Test non_integer_file"
        else:
            assert False, "FAIL Test non_integer_file"

    def test_out_of_map(self):
        # add "out_of_map_file.txt" in "invalid_files"
        try:
            load_config_file(f"{folder_path}/out_of_map_file.txt")
        except ArithmeticError as e:
            assert str(e) == "Invalid Configuration File: Wood contains a position that is out of map.", "FAIL Test out_of_map_file"
            print("out_of_map_file Pass")
        except Exception as e:
            print(e)
            assert not e, "FAIL Test out_of_map_file"
        else:
            assert False, "FAIL Test out_of_map_file"

    def test_occupy_home_or_next_to_home(self):
        # add two invalid files: "occupy_home_file.txt" and
        # "occupy_next_to_home_file.txt" in "invalid_files"
        try:
            load_config_file(f"{folder_path}/occupy_home_file.txt")
            load_config_file(f"{folder_path}/occupy_next_to_home_file.txt")
        except ValueError as e:
            assert str(e) == "Invalid Configuration File: The positions of home bases or the positions next to the home bases are occupied!", "FAIL Test occupy_home_file"
            print("occupy_home_file Pass")
        except Exception as e:
            print(e)
            assert not e, "FAIL Test occupy_home_file"
        else:
            assert False, "FAIL Test occupy_home_file"

        try:
            load_config_file(f"{folder_path}/occupy_next_to_home_file.txt")
        except ValueError as e:
            assert str(e) == "Invalid Configuration File: The positions of home bases or the positions next to the home bases are occupied!", "FAIL Test occupy_home_file"
            print("occupy_next_to_home Pass")
        except Exception as e:
            print(e)
            assert not e, "FAIL Test occupy_next_to_home"
        else:
            assert False, "FAIL Test occupy_next_to_home"

    def test_duplicate_position(self):
        # add two files: "dupli_pos_in_single_line.txt" and
        # "dupli_pos_in_multiple_lines.txt" in "invalid_files"
        try:
            load_config_file(f"{folder_path}/dupli_pos_in_single_line.txt")
        except SyntaxError as e:
            assert str(e) == "Invalid Configuration File: Duplicate position (2, 4)!", "FAIL Test dupli_pos_in_single_line or dupli_pos_in_multiple"
            print("dupli_pos_in_single_line Pass")
        except Exception as e:
            print(e)
            assert not e, "FAIL Test dupli_pos_in_single_line"
        else:
            assert False, "FAIL Test dupli_pos_in_single_line"

        try:
            load_config_file(f"{folder_path}/dupli_pos_in_multiple_lines.txt")
        except SyntaxError as e:
            assert str(e) == "Invalid Configuration File: Duplicate position (2, 4)!", "FAIL Test dupli_pos_in_single_line or dupli_pos_in_multiple"
            print("dupli_pos_in_multiple Pass")
        except Exception as e:
            print(e)
            assert not e, "FAIL Test dupli_pos_in_multiple"
        else:
            assert False, "FAIL Test dupli_pos_in_multiple"

    def test_odd_length(self):
        # add "odd_length_file.txt" in "invalid_files"
        try:
            load_config_file(f"{folder_path}/odd_length_file.txt")
        except SyntaxError as e:
            assert str(e) == "Invalid Configuration File: Water has an odd number of elements!", "FAIL Test odd_length_file"
            print("odd_length_file Pass")
        except Exception as e:
            print(e)
            assert not e, "FAIL Test Test odd_length_file"
        else:
            assert False, "FAIL Test Test odd_length_file"

    def test_valid_file(self):
        # no need to create file for this one, just test loading config.txt
        try:
            load_config_file(f"config.txt")
        except Exception as e:
            assert False, str(e)


# you can run this test file to check tests and load_config_file
if __name__ == "__main__":
    # test_file_not_found()
    # test_format_error()
    # test_frame_format_error()
    # test_frame_out_of_range()
    # test_non_integer()
    # test_out_of_map()
    # test_occupy_home_or_next_to_home()
    # test_duplicate_position()
    # test_odd_length()
    # test_valid_file()
    unittest.main()
