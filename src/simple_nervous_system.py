from PIL import Image
import os
import cv2

import numpy as np

class SimpleNervousSystem:
    """A simple nervous system meant to replicate early vision systems found in primative life forms"""
    def __init__(self):
        self.current_file_number = 0

    def open_and_convert(self, filename):
        self.image = Image.open(filename).convert('L')
        self.image_array = np.array(self.image)

    def save_image(self, folder):
        Image.fromarray(self.squared_image).save(folder + str(self.current_file_number), "JPEG")
        self.current_file_number += 1

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
        # print("Middle: ", middle, " Outside: ", outside, " Division Number: ", div_num)
        # if outside > middle:
        if (outside > (200.0 * div_num * 4)) and (middle < (50.0 * div_num * 12)):
            # print("Found vertical line")
            return (np.ones((div_num, div_num), dtype=float) * 255.0)
        else:
            return np.zeros((div_num, div_num), dtype=float)

    def find_horizontal_lines(self, div_num, cell):
        middle = np.sum(cell[6:10, :])
        outside = np.sum(cell[0:6, :]) + np.sum(cell[10:, :])
        # print("Middle: ", middle, " Outside: ", outside, " Division Number: ", div_num)
        # if outside > middle:
        if (outside > (200.0 * div_num * 4)) and (middle < (50.0 * div_num * 12)):
            print("Found horizontal line")
            return (np.ones((div_num, div_num), dtype=float) * 255.0)
        else:
            return np.zeros((div_num, div_num), dtype=float)

    def replace_with_v_lines(self, div_num, cell):
        # White squares represent squares with a vertical line in them
        total_sum = np.sum(cell)
        new_cell = np.zeros((div_num, div_num), dtype=float)
        if total_sum > (250.0 * div_num * div_num):
            new_cell[:, 6:10] = 255.0
        return new_cell

    def replace_with_h_lines(self, div_num, cell):
        total_sum = np.sum(cell)
        new_cell = np.zeros((div_num, div_num), dtype=float)
        if total_sum > (250.0 * div_num ** 2):
            new_cell[6:10, :] = 255.0
        return new_cell

    def combine_h_and_v_lines(self, vertical_image, horizontal_image):
        return vertical_image + horizontal_image

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


    def make_test_video(self):
        image_folder = 'lines_video'
        video_name = 'StarWarsLines.avi'
        frames_per_second = 2

        # images = [img for img in os.listdir(image_folder) if img.endswith(".jpeg")]
        images = [img for img in os.listdir(image_folder)]
        sorted_images = sorted(images)

        print(sorted_images[0])

        frame = cv2.imread(os.path.join(image_folder, sorted_images[0]))
        height, width, layers = frame.shape

        video = cv2.VideoWriter(video_name, 0, frames_per_second, (width, height))

        for image in sorted_images:
            video.write(cv2.imread(os.path.join(image_folder, image)))

        cv2.destroyAllWindows()
        video.release()

    def process_pictures(self):
        image_folder = '../star_wars'
        folder_to_save = 'lines_video/'
        image_frames = [img for img in os.listdir(image_folder) if img.endswith(".bmp")]
        sorted_frames = sorted(image_frames)
        print(sorted_frames[0])
        for frame in sorted_frames:
            sns.open_and_convert(image_folder + "/" + frame)
            # sns.square_through_array(4, sns.convert_to_squares)
            # sns.square_through_array(16, sns.find_horizontal_lines)
            sns.square_through_array(4, sns.convert_to_squares)
            sns.square_through_array(16, sns.find_vertical_lines)
            sns.square_through_array(16, sns.replace_with_v_lines)
            v_image = sns.squared_image


            sns.open_and_convert(image_folder + "/" + frame)
            sns.square_through_array(4, sns.convert_to_squares)
            sns.square_through_array(16, sns.find_horizontal_lines)
            sns.square_through_array(16, sns.replace_with_h_lines)
            h_image = sns.squared_image

            self.squared_image = sns.combine_h_and_v_lines(v_image, h_image)
#           print("Currently on frame: ", frame)

            sns.save_image(folder_to_save)

sns = SimpleNervousSystem()
sns.make_test_video()
# sns.process_pictures()
# sns.make_test_video()
# image_folder = '../star_wars'
# folder_to_save = 'squares_video/'
# image_frames = [img for img in os.listdir(image_folder) if img.endswith(".bmp")]
# sorted_frames = sorted(image_frames)
# print(sorted_frames[0])
# for frame in sorted_frames:
#     sns.open_and_convert(image_folder + "/" + frame)
#     sns.square_through_array(4, sns.convert_to_squares)
#     sns.save_image(folder_to_save)
#     print("Currently on frame: ", frame)

# sns.make_test_video()
# sns.open_and_convert("test2.bmp")
# sns.square_through_array(4, sns.convert_to_squares)
# sns.display_image()
# sns.square_through_array(16, sns.find_vertical_lines)
# sns.square_through_array(16, sns.replace_with_v_lines)
# v_image = sns.squared_image


# sns.open_and_convert("test2.bmp")
# sns.square_through_array(4, sns.convert_to_squares)
# sns.square_through_array(16, sns.find_horizontal_lines)
# sns.square_through_array(16, sns.replace_with_h_lines)
# h_image = sns.squared_image

# combined_image = sns.combine_h_and_v_lines(v_image, h_image)
# Image.fromarray(combined_image).show()
# # print(sns.get_size_of_pic()[0])
