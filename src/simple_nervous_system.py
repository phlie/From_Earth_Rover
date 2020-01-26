from PIL import Image
import numpy as np

class SimpleNervousSystem:
    """A simple nervous system meant to replicate early vision systems found in primative life forms"""
    def open_and_convert(self, filename):
        self.image = Image.open(filename).convert('L')
        self.image_array = np.array(self.image)

    def get_size_of_pic(self):
        return self.image_array.shape

    def convert_to_squares(self, div_num, cell):
        if np.sum(cell) > (128.0 * (div_num ** 2)):
            moded_cell = np.ones((div_num, div_num), dtype=float) * 255.0
        else:
            moded_cell = np.zeros((div_num, div_num), dtype=float)
        return moded_cell

    def find_vertical_lines(self, div_num, cell):
        middle = np.sum(cell[:, 6:10])
        outside = np.sum(cell[:, 0:6]) + np.sum(cell[:, 10:])
        print("Middle: ", middle, " Outside: ", outside, " Division Number: ", div_num)
        # if outside > middle:
        if (outside > (200.0 * div_num * 4)) and (middle < (50.0 * div_num * 12)):
            print("Found vertical line")
            return (np.ones((div_num, div_num), dtype=float) * 128.0)
        else:
            return np.zeros((div_num, div_num), dtype=float)

    def find_horizontal_lines(self, div_num, cell):
        middle = np.sum(cell[6:10, :])
        outside = np.sum(cell[0:6, :]) + np.sum(cell[10:, :])
        print("Middle: ", middle, " Outside: ", outside, " Division Number: ", div_num)
        # if outside > middle:
        if (outside > (200.0 * div_num * 4)) and (middle < (50.0 * div_num * 12)):
            print("Found horizontal line")
            return (np.ones((div_num, div_num), dtype=float) * 255.0)
        else:
            return np.zeros((div_num, div_num), dtype=float)

    def square_through_array(self, div_num, fn):
        img_array = self.image_array
        for y_cell in range(self.get_size_of_pic()[0] // div_num):
            yl_limit = y_cell * div_num
            yu_limit = y_cell * div_num + div_num
            for x_cell in range(self.get_size_of_pic()[1] // div_num):
                xl_limit = x_cell * div_num
                xu_limit = x_cell * div_num + div_num
                old_cell = img_array[yl_limit : yu_limit, xl_limit : xu_limit]
                # new_cell = self.convert_to_squares(div_num, old_cell)
                new_cell = fn(div_num, old_cell)
                img_array[yl_limit : yu_limit, xl_limit : xu_limit] = new_cell
        self.squared_image = img_array.copy()

    def display_image(self):
        Image.fromarray(self.squared_image).show()

sns = SimpleNervousSystem()

sns.open_and_convert("test2.bmp")
sns.square_through_array(4, sns.convert_to_squares)
sns.display_image()
sns.square_through_array(16, sns.find_vertical_lines)
sns.display_image()

sns.open_and_convert("test2.bmp")
sns.square_through_array(4, sns.convert_to_squares)
sns.square_through_array(16, sns.find_horizontal_lines)
sns.display_image()


print(sns.get_size_of_pic()[0])
