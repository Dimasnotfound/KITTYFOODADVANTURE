import pygame
import random
import pygame_gui
import time
import os
import sys
import pandas as pd
import csv


# Initialize Pygame
pygame.init()

# Game window dimensions
window_width = 1000
window_height = 600
# Colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)

# Kitty and food block size
kitty_size = 30
food_size = 30
chamber_size = 80

# Fonts
Font = "font/StardewValley.otf"
font_style = pygame.font.Font(Font, 30)
score_font = pygame.font.Font(Font, 17)
level_font = pygame.font.Font(Font, 25)
capacity_font = pygame.font.Font(Font, 25)
submit_font = pygame.font.Font(Font, 12)

# Game window
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Kitty's Food Adventure")

clock = pygame.time.Clock()

# Memuat musik latar belakang
pygame.mixer.music.load("audio/background_music.mp3")
pygame.mixer.music.play(-1)  # Memutar musik secara terus-menerus


class Kitty(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((kitty_size, kitty_size))
        self.image.fill(white)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def move(self, x_change, y_change):
        new_x = self.rect.x + x_change
        new_y = self.rect.y + y_change
        self.rect.x = max(0, min(new_x, window_width - kitty_size))
        self.rect.y = max(0, min(new_y, window_height - kitty_size))

    def update(self):
        # pygame.draw.rect(window, white, self.rect)
        pass


class Item(pygame.sprite.Sprite):
    def __init__(self, position, image_path, weight, fullness):
        super().__init__()
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (food_size, food_size))
        self.rect = self.image.get_rect()
        self.rect.x = position[0]
        self.rect.y = position[1]
        self.weight = weight
        self.fullness = fullness


class Level:
    def __init__(self, level_num, max_weight):
        self.level_num = level_num
        self.max_weight = max_weight


def generate_food(level):
    chamber_position = [window_width // 2 - chamber_size //
                        2, window_height // 2 - chamber_size // 2]
    food_list = []
    excluded_areas = [
        (0, 0, 200, 150),  # Area kiri atas
        (window_width - 150, 0, 150, 150),  # Area kanan atas
        (450, 200, 150, 150)  # Area tertentu
    ]

    fullness_set = set()  # Set untuk menyimpan nilai kenyang yang sudah tergenerasi

    for _ in range(2 + level.level_num):
        valid_position = False
        position = None

        while not valid_position:
            position = (
                random.randint(chamber_size, window_width -
                               food_size - chamber_size - food_size),
                random.randint(chamber_size, window_height -
                               food_size - chamber_size - food_size)
            )

            is_position_valid = all(
                abs(position[0] - food["position"][0]) >= food_size and
                abs(position[1] - food["position"][1]) >= food_size
                for food in food_list
            )

            is_position_within_chamber = (
                chamber_position[0] <= position[0] <= chamber_position[0] + chamber_size and
                chamber_position[1] <= position[1] <= chamber_position[1] + chamber_size
            )

            is_position_in_excluded_area = any(
                excluded_area[0] <= position[0] <= excluded_area[0] + excluded_area[2] and
                excluded_area[1] <= position[1] <= excluded_area[1] +
                excluded_area[3]
                for excluded_area in excluded_areas
            )

            if is_position_valid and not is_position_within_chamber and not is_position_in_excluded_area:
                valid_position = True

        image_path = random.choice(os.listdir("food"))
        image_path = os.path.join("food", image_path)

        # Generate nilai kenyang baru yang belum tergenerasi sebelumnya
        weight = random.randint(1, level.max_weight)
        fullness = random.randint(1, level.level_num * 10)
        while fullness in fullness_set:
            fullness = random.randint(1, level.level_num * 10)

        fullness_set.add(fullness)

        food = {
            "position": position,
            "image_path": image_path,
            "weight": weight,
            "fullness": fullness
        }
        food_list.append(food)

    return food_list


def draw_food(position, image, weight, fullness):
    window.blit(image, position)
    weight_text = score_font.render("W: " + str(weight), True, (41, 29, 49))
    fullness_text = score_font.render(
        "F: " + str(fullness), True, (41, 29, 49))
    text_x = position[0] + (food_size - weight_text.get_width()) // 2
    text_y = position[1] - weight_text.get_height() - 5
    window.blit(weight_text, [text_x, text_y])
    text_x = position[0] + (food_size - fullness_text.get_width()) // 2
    text_y = position[1] - fullness_text.get_height() - 5 - \
        weight_text.get_height()
    window.blit(fullness_text, [text_x, text_y])


def draw_chamber(position, in_chamber):
    pygame.draw.rect(
        window, red, [position[0], position[1], chamber_size, chamber_size], 2)
    if in_chamber:
        submit_rect_width = 80
        submit_rect_height = 40
        submit_rect_x = position[0] + \
            (chamber_size - submit_rect_width) // 2
        submit_rect_y = position[1] + chamber_size + 10
        submit_rect = pygame.Rect(
            submit_rect_x, submit_rect_y, submit_rect_width, submit_rect_height)
        pygame.draw.rect(window, (207, 87, 60), submit_rect)
        submit_text = submit_font.render("Press [SPACE]", True, white)
        submit_text_rect = submit_text.get_rect(center=submit_rect.center)
        window.blit(submit_text, submit_text_rect)


def display_level(level):
    level_text = level_font.render(
        "Level: " + str(level.level_num), True, (41, 29, 49))
    window.blit(level_text, [window_width - level_text.get_width() - 20, 20])


def display_fullness(fullness):
    value = level_font.render("Fullness: " + str(fullness), True, (41, 29, 49))
    window.blit(value, [20, 20])


def display_capacity(capacity, max_weight):
    capacity_text = capacity_font.render(
        "Weight: " + str(capacity) + "/" + str(max_weight), True, (41, 29, 49))
    window.blit(capacity_text, [20, 50])


def display_chance(chance):
    chances_text = capacity_font.render(
        "Chances: " + str(chance), True, (41, 29, 49))
    window.blit(chances_text, (window_width -
                chances_text.get_width() - 20, 50))


def display_time(elapsed_time):
    elapsed_time_in_seconds = int(elapsed_time)
    chances_text = capacity_font.render(
        "Time: " + str(elapsed_time_in_seconds) + "s", True, (41, 29, 49))
    window.blit(chances_text, (window_width -
                chances_text.get_width() - 20, 80))


def display_total_fullness(total_fullness):
    fullness_text = capacity_font.render(
        "Total Fullness: " + str(total_fullness), True, (41, 29, 49))
    window.blit(fullness_text, [20, 80])


def display_score(total_fullness, elapsed_time, chance):
    score = (total_fullness / elapsed_time) + 10 + chance
    rounded_score = round(score, 2)
    result_text = capacity_font.render(
        "Score: " + str(rounded_score), True, (41, 29, 49))
    window.blit(result_text, [20, 50])


def knapsack_algorithm(food_list, max_weight):
    n = len(food_list)
    dp = [[0] * (max_weight + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for w in range(1, max_weight + 1):
            if food_list[i - 1]["weight"] <= w:
                dp[i][w] = max(food_list[i - 1]["fullness"] + dp[i - 1]
                                [w - food_list[i - 1]["weight"]], dp[i - 1][w])
            else:
                dp[i][w] = dp[i - 1][w]

    selected_food_program = []
    w = max_weight
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            selected_food_program.append(food_list[i - 1])
            w -= food_list[i - 1]["weight"]

    return selected_food_program


def meminta_nama():
    window = pygame.display.set_mode((window_width, window_height))
    manager = pygame_gui.UIManager((window_width, window_height))

    background_img = pygame.image.load("img/background.png").convert()
    background_img = pygame.transform.scale(
        background_img, (window_width, window_height))

    # Memuat efek suara
    button_click_sound = pygame.mixer.Sound("audio/button_sound.wav")

    button_width = 150
    button_height = 64
    button_padding = 30
    button_x = (window_width - (button_width + button_padding) * 1.8) // 2
    button_y = 300

    text_box_width = 300
    text_box_height = 40
    text_box_x = (window_width - text_box_width) // 2
    text_box_y = (window_height - text_box_height) // 2 - 30
    show_leaderboard = False

    logo_img = pygame.image.load("img/logo.png")
    logo_width = 400
    logo_height = 101
    logo_x = (window_width - logo_width) // 2
    logo_y = text_box_y - logo_height - 20
    logo_img_original = pygame.transform.scale(
        logo_img, (logo_width, logo_height))

    fullness_text = capacity_font.render(
        "Enter Name", True, (41, 29, 49))

    text_box = pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect(
            (text_box_x, text_box_y), (text_box_width, text_box_height)),
        manager=manager
    )

    start_button_img = pygame.image.load("img/start_button.png")
    start_button_img_original = pygame.transform.scale(
        start_button_img, (button_width, button_height))
    exit_button_img = pygame.image.load("img/exit_button.png")
    exit_button_img_original = pygame.transform.scale(
        exit_button_img, (button_width, button_height))
    leaderboard_button_img = pygame.image.load("img/leaderboard_button.png")
    leaderboard_button_img_original = pygame.transform.scale(
        leaderboard_button_img, (button_width, button_height))

    start_button_rect = pygame.Rect(
        (button_x, button_y), (button_width, button_height))
    exit_button_rect = pygame.Rect(
        (button_x + button_width + button_padding, button_y), (button_width, button_height))
    leaderboard_button_rect = pygame.Rect(
        (button_x * 1.277, button_y - 30 + button_height + button_padding), (button_width, button_height))

    clock = pygame.time.Clock()
    running = True
    while running:
        time_delta = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    text_box.set_text(text_box.get_text()[:-1])
            manager.process_events(event)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button_rect.collidepoint(mouse_pos):
                    button_click_sound.play()  # Memainkan suara saat tombol Start diklik
                    nama = text_box.get_text()
                    kitty_game(nama)
                    running = False

                if exit_button_rect.collidepoint(mouse_pos):
                    button_click_sound.play()  # Memainkan suara saat tombol exit diklik
                    print('exit')
                    time.sleep(1)  # Delay selama 1 detik
                    pygame.quit()
                    sys.exit()

                if leaderboard_button_rect.collidepoint(mouse_pos):
                    button_click_sound.play()  # Memainkan suara saat tombol score diklik
                    window.fill((0, 0, 0))
                    show_leaderboard = True
                    running = False

        manager.update(time_delta)
        mouse_pos = pygame.mouse.get_pos()

        if start_button_rect.collidepoint(mouse_pos):
            start_button_rect_scaled = pygame.Rect(start_button_rect.left - int(button_width * 0.1),
                                                   start_button_rect.top -
                                                   int(button_height * 0.1),
                                                   int(button_width * 1.2),
                                                   int(button_height * 1.2))
            start_button_img_scaled = pygame.transform.scale(start_button_img_original,
                                                             (start_button_rect_scaled.width,
                                                              start_button_rect_scaled.height))
        else:
            start_button_rect_scaled = start_button_rect
            start_button_img_scaled = start_button_img_original

        if exit_button_rect.collidepoint(mouse_pos):
            exit_button_rect_scaled = pygame.Rect(exit_button_rect.left - int(button_width * 0.1),
                                                  exit_button_rect.top -
                                                  int(button_height * 0.1),
                                                  int(button_width * 1.2),
                                                  int(button_height * 1.2))
            exit_button_img_scaled = pygame.transform.scale(exit_button_img_original,
                                                            (exit_button_rect_scaled.width,
                                                             exit_button_rect_scaled.height))
        else:
            exit_button_rect_scaled = exit_button_rect
            exit_button_img_scaled = exit_button_img_original

        if leaderboard_button_rect.collidepoint(mouse_pos):
            leaderboard_button_rect_scaled = pygame.Rect(leaderboard_button_rect.left - int(button_width * 0.1),
                                                         leaderboard_button_rect.top -
                                                         int(button_height * 0.1),
                                                         int(button_width * 1.2),
                                                         int(button_height * 1.2))
            leaderboard_button_img_scaled = pygame.transform.scale(leaderboard_button_img_original,
                                                                   (leaderboard_button_rect_scaled.width,
                                                                    leaderboard_button_rect_scaled.height))
        else:
            leaderboard_button_rect_scaled = leaderboard_button_rect
            leaderboard_button_img_scaled = leaderboard_button_img_original

        # Menampilkan gambar latar belakang
        window.blit(background_img, (0, 0))
        window.blit(logo_img_original, (logo_x, logo_y))
        window.blit(start_button_img_scaled, start_button_rect_scaled)
        window.blit(exit_button_img_scaled, exit_button_rect_scaled)
        window.blit(leaderboard_button_img_scaled,
                    leaderboard_button_rect_scaled)
        window.blit(fullness_text, [
                    (window_width)//2 - 50, (window_height)//2 - 75])
        manager.draw_ui(window)

        if show_leaderboard:
            display_csv_data()

        pygame.display.flip()
        pygame.display.update()


def quick_sort(data):
    if len(data) <= 1:
        return data

    pivot = data[0][1]  # Gunakan skor sebagai pivot
    smaller = []
    equal = []
    larger = []

    for item in data:
        if item[1] < pivot:
            smaller.append(item)
        elif item[1] == pivot:
            equal.append(item)
        else:
            larger.append(item)

    return quick_sort(larger) + equal + quick_sort(smaller)


def display_csv_data():
    pygame.init()

    # Inisialisasi ukuran jendela
    window_width = 1000
    window_height = 600

    window = pygame.display.set_mode((window_width, window_height))
    background_img = pygame.image.load("img/background1.png").convert()
    background_img = pygame.transform.scale(
        background_img, (window_width, window_height))
    window.blit(background_img, (0, 0))

    # Fungsi untuk tombol "Exit" pada leaderboard
    def button_exit_leaderboard():
        button_click_sound.play()
        meminta_nama()
    # Memuat efek suara
    button_click_sound = pygame.mixer.Sound("audio/button_sound.wav")

    running = True
    button_hovered_prev = False  # Menyimpan status tombol hover sebelumnya
    while running:
        # Menghandle event pygame
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Pemrosesan klik tombol exit
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if exit_button_rect.collidepoint(mouse_pos):
                    button_exit_leaderboard()
                    running = False

        # Proses pengambilan data dan tampilan leaderboard
        data = []
        with open('data/data_user.csv', 'r') as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                data.append(row)

        data = quick_sort(data)  # Urutkan data menggunakan Quick Sort
        data = data[:5]  # Batasi hanya 5 data

        font = pygame.font.Font(Font, 22)
        cell_width = 100
        cell_height = 60
        table_width = cell_width * len(data[0])
        table_height = cell_height * len(data)
        table_x = (window_width - table_width) // 2
        table_y = 140

        # Gambar latar belakang tabel
        table_image = pygame.image.load("img/table_background1.png")
        table_image = pygame.transform.scale(
            table_image, (table_width, table_height))
        window.blit(table_image, (table_x, table_y))

        # Tampilkan isi tabel
        x_pos = table_x + 40
        y_pos = table_y + 50
        for row in data:
            for col_index, col_value in enumerate(row):
                text = font.render(col_value, True, (0, 0, 0))
                window.blit(text, (x_pos, y_pos))
                x_pos += cell_width - 10
            y_pos += 70 - 25
            x_pos = table_x + 40

        # Tampilkan tombol Exit
        button_width = 150
        button_height = 64
        button_hover_scale = 1.2  # Skala perbesaran saat tombol diperbesar
        button_x = (window_width - button_width) // 2
        button_y = window_height - 100  # Ubah posisi tombol di bawah tabel
        # Mendeklarasikan status tombol saat kursor mouse mendekat
        button_hovered = False

        exit_button = pygame.image.load("img/exit_button.png")
        exit_button = pygame.transform.scale(
            exit_button, (button_width, button_height))
        exit_button_rect = exit_button.get_rect()
        exit_button_rect.center = (
            button_x + button_width // 2, button_y + button_height // 2)

        # Mendapatkan posisi mouse
        mouse_pos = pygame.mouse.get_pos()
        # Mengecek apakah kursor mouse berada di atas tombol
        if exit_button_rect.collidepoint(mouse_pos):
            button_hovered = True

        # Update jendela
        pygame.display.flip()
        pygame.display.update()

        # Menghapus gambar tombol yang diperbesar jika tidak di-hover lagi
        if button_hovered_prev and not button_hovered:
            # Perbesar area penghapusan sedikit lebih luas
            pygame.draw.rect(window, (255, 215, 137), (exit_button_rect.x - 15,
                             exit_button_rect.y - 5, exit_button_rect.width + 25, exit_button_rect.height + 10))

        # Tampilkan tombol Exit
        if button_hovered:
            scaled_width = int(button_width * button_hover_scale)
            scaled_height = int(button_height * button_hover_scale)
            scaled_x = button_x - (scaled_width - button_width) // 2
            scaled_y = button_y - (scaled_height - button_height) // 2
            scaled_button_rect = pygame.Rect(
                scaled_x, scaled_y, scaled_width, scaled_height)
            exit_button_image_scaled = pygame.transform.scale(
                exit_button, (scaled_width, scaled_height))
            window.blit(exit_button_image_scaled, scaled_button_rect)
        else:
            window.blit(exit_button, exit_button_rect)

        # Simpan status tombol hover saat ini sebagai tombol hover sebelumnya
        button_hovered_prev = button_hovered


def display_nama(nama):
    capacity_text = capacity_font.render(
        "Player: " + str(nama), True, (41, 29, 49))
    window.blit(capacity_text, [20, 20])


def button_exit():
    button_width = 150
    button_height = 64
    button_hover_scale = 1.2  # Skala perbesaran saat tombol diperbesar

    button_x = (window_width - button_width) // 2
    button_y = (window_height - button_height) // 2

    # Memuat gambar exit button
    exit_button_image = pygame.image.load("img/exit_button.png")
    exit_button_image = pygame.transform.scale(
        exit_button_image, (button_width, button_height))
    button_click_sound = pygame.mixer.Sound("audio/button_sound.wav")

    # Mendefinisikan ukuran dan posisi tombol
    button_rect = pygame.Rect(button_x, button_y, button_width, button_height)

    # Mendeklarasikan status tombol saat kursor mouse mendekat
    button_hovered = button_rect.collidepoint(pygame.mouse.get_pos())

    # Menggambar tombol exit yang tidak ter-hover
    window.blit(exit_button_image, button_rect)

    # Mengecek apakah tombol exit diklik
    if button_hovered and pygame.mouse.get_pressed()[0] == 1:
        button_click_sound.play()
        time.sleep(1)
        pygame.quit()
        sys.exit()

    # Menggambar tombol exit yang ter-hover di atas tombol exit yang tidak ter-hover
    if button_hovered:
        scaled_width = int(button_width * button_hover_scale)
        scaled_height = int(button_height * button_hover_scale)
        scaled_x = button_x - (scaled_width - button_width) // 2
        scaled_y = button_y - (scaled_height - button_height) // 2
        scaled_button_rect = pygame.Rect(
            scaled_x, scaled_y, scaled_width, scaled_height)
        exit_button_image_scaled = pygame.transform.scale(
            exit_button_image, (scaled_width, scaled_height))

        # Menggambar tombol exit yang ter-hover
        window.blit(exit_button_image_scaled, scaled_button_rect)

    # Menggambar tombol dengan ukuran yang sesuai berdasarkan status button_hovered
    if button_hovered:
        window.blit(exit_button_image, button_rect)
    else:
        window.blit(exit_button_image, (button_x, button_y))


def check_equality(list1, list2):
    if len(list1) != len(list2):
        return False

    for item1 in list1:
        found = False
        for item2 in list2:
            if item1["position"] == item2["position"] and item1["image_path"] == item2["image_path"] and item1["weight"] == item2["weight"] and item1["fullness"] == item2["fullness"]:
                found = True
                break
        if not found:
            return False

    return True


def drawGrid():
    blockSize = 50  # Set the size of the grid block
    for x in range(0, window_width, blockSize):
        for y in range(0, window_height, blockSize):
            rect = pygame.Rect(x, y, blockSize, blockSize)
            pygame.draw.rect(window, white, rect, 1)


def simpan_ke_csv(nama, total_fullness, rounded_score, current_level_index, time_cvt):
    data = {
        'Nama': [nama],
        'Fullness': [total_fullness],
        'Score': [rounded_score],
        'Level': [current_level_index],
        'Time': [str(time_cvt) + "s"]
    }

    df = pd.DataFrame(data)

    # Cek apakah file CSV sudah ada sebelumnya
    try:
        existing_data = pd.read_csv('data/data_user.csv')
        df = pd.concat([existing_data, df], ignore_index=True)
    except FileNotFoundError:
        pass

    df.to_csv('data/data_user.csv', index=False)


def kitty_game(nama):
    #####################################
    ############# WALKING#################
    #####################################

    sprites_walking_east = [
        pygame.image.load("img/character/walking/east/walking_east_0.png"),
        pygame.image.load("img/character/walking/east/walking_east_1.png"),
        pygame.image.load("img/character/walking/east/walking_east_2.png"),
        pygame.image.load("img/character/walking/east/walking_east_3.png")
    ]

    sprites_walking_north = [
        pygame.image.load("img/character/walking/north/walking_north_0.png"),
        pygame.image.load("img/character/walking/north/walking_north_1.png"),
        pygame.image.load("img/character/walking/north/walking_north_2.png"),
        pygame.image.load("img/character/walking/north/walking_north_3.png")
    ]

    sprites_walking_south = [
        pygame.image.load("img/character/walking/south/walking_south_0.png"),
        pygame.image.load("img/character/walking/south/walking_south_1.png"),
        pygame.image.load("img/character/walking/south/walking_south_2.png"),
        pygame.image.load("img/character/walking/south/walking_south_3.png")
    ]

    sprites_walking_west = [
        pygame.image.load("img/character/walking/west/walking_west_0.png"),
        pygame.image.load("img/character/walking/west/walking_west_1.png"),
        pygame.image.load("img/character/walking/west/walking_west_2.png"),
        pygame.image.load("img/character/walking/west/walking_west_3.png")
    ]

    #####################################
    ########### SITTING DOWN##############
    #####################################

    sprites_sitting_down_east = [
        pygame.image.load(
            "img/character/sitting_down/east/sitting_down_east_0.png"),
        pygame.image.load(
            "img/character/sitting_down/east/sitting_down_east_1.png"),
        pygame.image.load(
            "img/character/sitting_down/east/sitting_down_east_2.png"),
        pygame.image.load(
            "img/character/sitting_down/east/sitting_down_east_3.png"),
        pygame.image.load(
            "img/character/sitting_down/east/sitting_down_east_4.png"),
        pygame.image.load(
            "img/character/sitting_down/east/sitting_down_east_5.png")
    ]

    sprites_sitting_down_north = [
        pygame.image.load(
            "img/character/sitting_down/north/sitting_down_north_0.png"),
        pygame.image.load(
            "img/character/sitting_down/north/sitting_down_north_1.png"),
        pygame.image.load(
            "img/character/sitting_down/north/sitting_down_north_2.png"),
        pygame.image.load(
            "img/character/sitting_down/north/sitting_down_north_3.png"),
        pygame.image.load(
            "img/character/sitting_down/north/sitting_down_north_4.png"),
        pygame.image.load(
            "img/character/sitting_down/north/sitting_down_north_5.png")
    ]

    sprites_sitting_down_south = [
        pygame.image.load(
            "img/character/sitting_down/south/sitting_down_south_0.png"),
        pygame.image.load(
            "img/character/sitting_down/south/sitting_down_south_1.png"),
        pygame.image.load(
            "img/character/sitting_down/south/sitting_down_south_2.png"),
        pygame.image.load(
            "img/character/sitting_down/south/sitting_down_south_3.png"),
        pygame.image.load(
            "img/character/sitting_down/south/sitting_down_south_4.png"),
        pygame.image.load(
            "img/character/sitting_down/south/sitting_down_south_5.png")
    ]

    sprites_sitting_down_west = [
        pygame.image.load(
            "img/character/sitting_down/west/sitting_down_west_0.png"),
        pygame.image.load(
            "img/character/sitting_down/west/sitting_down_west_1.png"),
        pygame.image.load(
            "img/character/sitting_down/west/sitting_down_west_2.png"),
        pygame.image.load(
            "img/character/sitting_down/west/sitting_down_west_3.png"),
        pygame.image.load(
            "img/character/sitting_down/west/sitting_down_west_4.png"),
        pygame.image.load(
            "img/character/sitting_down/west/sitting_down_west_5.png")
    ]

    ############################### END SPRITES#########################
    pygame.mixer.music.set_volume(0.5)
    current_direction = "south"
    current_sprites = sprites_sitting_down_south
    # Kitty initial position
    kitty = Kitty(window_width // 2 - kitty_size // 2,
                  window_height // 2 - kitty_size // 2)
    background_image = pygame.image.load("img/bg_game.png")
    background_image = pygame.transform.scale(
        background_image, (window_width, window_height))

    sprite_rect = sprites_walking_east[0].get_rect()

    sprite_rect.centerx = window_width // 2
    sprite_rect.centery = window_height // 2

    speed = 3

    current_frame = 0

    # Game variables
    chance = 3
    last_space_press_time = 0
    knapsack_weight = 0
    fullness = 0
    current_level_index = 0
    total_fullness = 0

    # Direktori file suara
    sound_directory = "audio/catsound/"

    # Daftar nama file suara
    sound_files = os.listdir(sound_directory)

    # Load suara ke dalam list
    sounds = []
    for file in sound_files:
        sound_path = os.path.join(sound_directory, file)
        sound = pygame.mixer.Sound(sound_path)
        sounds.append(sound)

    # Inisialisasi DataFrame

    levels = [
        Level(1, 10),
        Level(2, 20),
        Level(3, 30),
        Level(4, 40),
        Level(5, 50)
    ]
    selected_food = []
    total_selected_food_level = 0

    generated_food = generate_food(levels[current_level_index])

    selected_food_program = knapsack_algorithm(
        generated_food, levels[current_level_index].max_weight)

    chamber_position = [window_width // 2 - chamber_size //
                        2, window_height // 2 - chamber_size // 2]
    in_chamber = False
    game_over = False

    # Create sprite groups
    all_sprites = pygame.sprite.Group()
    items = pygame.sprite.Group()

    # Create items for the new level
    for food in generated_food:
        item = Item(food["position"], food["image_path"],
                    food["weight"], food["fullness"])
        items.add(item)
        all_sprites.add(item)

    is_game_finished = False
    chamber_active = True
    simpan_csv = True
    # Waktu awal program berjalan
    start_time = time.time()

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        if not is_game_finished:
            end_time = time.time()
            elapsed_time = end_time - start_time

        if is_game_finished:
            generated_food = []
            items.empty()
            all_sprites.empty()

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            sprite_rect.x -= speed
            current_direction = "west"
            current_sprites = sprites_walking_west
            current_frame += 0.3
            kitty.move(-3, 0)
            is_sitting_down = False

        elif keys[pygame.K_RIGHT]:
            sprite_rect.x += speed
            current_direction = "east"
            current_sprites = sprites_walking_east
            current_frame += 0.3
            kitty.move(3, 0)
            is_sitting_down = False

        elif keys[pygame.K_UP]:
            sprite_rect.y -= speed
            current_direction = "north"
            current_sprites = sprites_walking_north
            current_frame += 0.3
            kitty.move(0, -3)
            is_sitting_down = False

        elif keys[pygame.K_DOWN]:
            sprite_rect.y += speed
            current_direction = "south"
            current_sprites = sprites_walking_south
            current_frame += 0.3
            kitty.move(0, 3)
            is_sitting_down = False

        else:
            is_sitting_down = True

        # Batasi karakter agar tidak keluar dari layar
        if sprite_rect.left < 0:
            sprite_rect.left = 0
        if sprite_rect.right > window_width:
            sprite_rect.right = window_width
        if sprite_rect.top < 0:
            sprite_rect.top = 0
        if sprite_rect.bottom > window_height:
            sprite_rect.bottom = window_height

        window.fill((0, 0, 0))

        if current_frame >= len(current_sprites):
            current_frame = 0
        if current_frame == 8:
            current_frame = 0

        window.blit(background_image, (0, 0))

        if is_sitting_down:
            if current_direction == "west":
                current_sprites = sprites_sitting_down_west
            elif current_direction == "east":
                current_sprites = sprites_sitting_down_east
            elif current_direction == "north":
                current_sprites = sprites_sitting_down_north
            elif current_direction == "south":
                current_sprites = sprites_sitting_down_south

        window.blit(current_sprites[int(current_frame)], sprite_rect)
        if kitty.rect.colliderect(pygame.Rect(chamber_position[0], chamber_position[1], chamber_size, chamber_size)) and chamber_active:
            in_chamber = True
        else:
            in_chamber = False

        if in_chamber:
            # print(selected_food_program)  # KUNCI JAWABAN
            if keys[pygame.K_SPACE]:
                current_time = time.time()
                if current_time - last_space_press_time >= 0.5:
                    last_space_press_time = current_time
                    if check_equality(selected_food, selected_food_program):
                        levelup_sound = pygame.mixer.Sound("audio/levelup.mp3")
                        levelup_sound.play()
                        chance += 1
                        total_selected_food_level = 0
                        selected_food.clear()
                        print("Selected food and selected food program are the same.")

                        # Cek apakah semua makanan telah dipilih
                        current_level_index += 1
                        print(current_level_index)
                        fullness = 0
                        knapsack_weight = 0
                        if current_level_index >= len(levels):
                            is_game_finished = True
                            chamber_active = False
                            print("Congratulations! You completed all levels.")
                        else:
                            selected_food = []
                            generated_food = generate_food(
                                levels[current_level_index])
                            chamber_position = [
                                window_width // 2 - chamber_size // 2, window_height // 2 - chamber_size // 2]
                            selected_food_program = knapsack_algorithm(
                                generated_food, levels[current_level_index].max_weight)

                    else:
                        failure_sound = pygame.mixer.Sound("audio/failure.wav")
                        failure_sound.play()
                        chance -= 1
                        fullness = 0
                        knapsack_weight = 0
                        total_fullness -= total_selected_food_level
                        # Mengembalikan total_fullness ke nilai sebelumnya
                        print(
                            "Selected food and selected food program are different.")
                        selected_food.clear()
                        total_selected_food_level = 0
                        if chance == 0:
                            is_game_finished = True
                            chamber_active = False
                            print("game over")

                        # Generate makanan ulang di level yang sama
                        generated_food = generate_food(
                            levels[current_level_index])
                        selected_food_program = knapsack_algorithm(
                            generated_food, levels[current_level_index].max_weight)

        for food in generated_food:
            if kitty.rect.colliderect(pygame.Rect(food["position"][0], food["position"][1], food_size, food_size)):
                if len(selected_food) < levels[current_level_index].max_weight and knapsack_weight + food["weight"] <= levels[current_level_index].max_weight:
                    random_sound = random.choice(sounds)
                    random_sound.play()
                    selected_food.append(food)
                    generated_food.remove(food)
                    fullness += food["fullness"]
                    knapsack_weight += food["weight"]
                    for sprite in all_sprites:
                        if sprite.rect.x == food["position"][0] and sprite.rect.y == food["position"][1]:
                            sprite.kill()
                    total_selected_food_level += food["fullness"]
                    total_fullness += food["fullness"]

        kitty.update()

        for food in generated_food:
            image = pygame.image.load(food["image_path"])
            draw_food(food["position"], image,
                      food["weight"], food["fullness"])

        if chamber_active:
            draw_chamber(chamber_position, in_chamber)

        display_time(elapsed_time)
        display_total_fullness(total_fullness)
        if current_level_index < len(levels) and chance > 0:
            # drawGrid() #membuat grid
            display_chance(chance)
            display_fullness(fullness)
            display_level(levels[current_level_index])
            display_capacity(
                knapsack_weight, levels[current_level_index].max_weight)
        else:
            time_cvt = int(elapsed_time)
            score = (total_fullness / elapsed_time) + 10 + chance
            rounded_score = round(score, 2)
            if simpan_csv:
                simpan_ke_csv(nama, total_fullness, rounded_score,
                              current_level_index, time_cvt)
                simpan_csv = False
            display_score(total_fullness, elapsed_time, chance)
            display_nama(nama)
            button_exit()

        pygame.display.update()
        clock.tick(30)


meminta_nama()
