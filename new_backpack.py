import os
import sqlite3
import sys
import pygame
from pygame.locals import *


if __name__ == "__main__":

    class Item:
        """
        Этот класс представляет из себя предмет.
        """
        def __init__(self, name, image):
            self.name = name
            self.image = image


    class ItemCell:
        """
        Этот класс представляет из себя ячейку, содержащую предмет.
        """
        def __init__(self, pos, cell_size=(75, 75), item=None):
            self.pos = pos
            self.rect = Rect(*pos, *cell_size)
            self.item = item

        def check_for_input(self, pos):
            if not self.rect.collidepoint(pos):
                return
            global held_item
            self.item, held_item = held_item, self.item

        def draw_item(self):
            if self.item is None:
                return
            screen.blit(self.item.image, self.pos)

        def get_item_name(self):
            return self.item.name


    class EquipCell(ItemCell):
        """
        Этот класс представляет из себя ячейку, содержащую надетый предмет.
        """
        def __init__(self, pos, cell_size=(150, 150), item=None, is_first=True):
            super().__init__(pos, cell_size, item)
            self.is_first = is_first

        def check_for_input(self, pos):
            if not self.rect.collidepoint(pos):
                return

            global held_item
            if self.item is not None:
                held_item, self.item = self.item, held_item

                if self.is_first:
                    if held_item is not None and self.item is not None:
                        first = self.get_item_name()
                    else:
                        first = ""
                    second = cursor.execute("SELECT second FROM equipped_items").fetchone()[0]
                    cursor.execute(f"""
                        UPDATE equipped_items
                            SET first = "{first}"
                            WHERE second = "{second}"
                    """)
                else:
                    if held_item is not None and self.item is not None:
                        second = self.get_item_name()
                    else:
                        second = ""
                    first = cursor.execute("SELECT first FROM equipped_items").fetchone()[0]
                    cursor.execute(f"""
                        UPDATE equipped_items
                            SET second = "{second}"
                            WHERE first = "{first}"
                    """)
                connection.commit()
            else:
                if held_item is None:
                    return

                self.item, held_item = held_item, self.item

                if self.is_first:
                    second = cursor.execute("SELECT second FROM equipped_items").fetchone()[0]
                    cursor.execute(f"""
                        UPDATE equipped_items
                            SET first = "{self.get_item_name()}"
                            WHERE second = "{second}"
                    """)
                else:
                    first = cursor.execute("SELECT first FROM equipped_items").fetchone()[0]
                    cursor.execute(f"""
                        UPDATE equipped_items
                            SET second = "{self.get_item_name()}"
                            WHERE first = "{first}"
                    """)
                connection.commit()

        def draw_item(self):
            if self.item is None:
                return
            x, y = self.pos
            screen.blit(self.item.image, (x + 50, y + 50))

    def get_equipped_items():
        return cursor.execute("SELECT first, second FROM equipped_items").fetchone()

    def get_empty_cell():
        for cell in loot_cells:
            if cell.item is None:
                return cell

    def is_database_corrupted():
        """
        Проверяет, повреждена ли база данных.
        :return: повреждена ли база данных.
        """
        global cursor
        table = cursor.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name='equipped_items';").fetchone()
        if not table:
            return True
        columns = cursor.execute("SELECT COUNT(*) FROM pragma_table_info('equipped_items')").fetchone()
        return columns[0] < 2

    def create_table():
        """
        Создаёт таблицу в базе данных.
        """
        global connection, cursor

        connection = sqlite3.connect("Sql/data.sqlite")
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE equipped_items (
                first  TEXT UNIQUE
                            NOT NULL,
                second TEXT UNIQUE
                            NOT NULL
            );
        """)
        cursor.execute("INSERT INTO equipped_items VALUES ('', '')")
        connection.commit()

    connection, cursor = None, None
    if not os.path.isfile("Sql/data.sqlite"):
        create_table()
    else:
        connection = sqlite3.connect("Sql/data.sqlite")
        cursor = connection.cursor()
        if is_database_corrupted():
            print("База данных повреждена.")
            sys.exit()

    pygame.init()
    size = width, height = 600, 600

    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Рюкзак")

    clock = pygame.time.Clock()

    backpack_bg = pygame.image.load(" Background/Backpack.png").convert()

    equip_cells = [
        EquipCell((45, 50), is_first=True), EquipCell((405, 50), is_first=False)
    ]

    loot_cells = [
        ItemCell((47, 360)), ItemCell((200, 360)),
        ItemCell((350, 360)), ItemCell((503, 360)),
        ItemCell((47, 475)), ItemCell((200, 475)),
        ItemCell((350, 475)), ItemCell((503, 475)),
    ]

    items = {
        "Полнолуние": Item("Полнолуние", pygame.image.load("Loot/loot1.png").convert_alpha()),
        "Ласточка": Item("Ласточка", pygame.image.load("Loot/loot2.png").convert_alpha()),
        "Филин": Item("Филин", pygame.image.load("Loot/loot3.png").convert_alpha()),
        "Бякко": Item("Бякко", pygame.image.load("Loot/loot4.png").convert_alpha()),
        "Черная дурь": Item("Черная дурь", pygame.image.load("Loot/loot5.png").convert_alpha()),
        "": None
    }

    items_left = items

    for n, item in enumerate(get_equipped_items()):
        if item == "":
            continue
        equip_cells[n].item = items[item]
        items_left[item] = None

    for key, item in items_left.items():
        cell = get_empty_cell()
        cell.item = item

    held_item = None

    running = True
    while running:
        keys = pygame.key.get_pressed()
        screen.blit(backpack_bg, (0, 0))
        for cell in loot_cells:
            cell.draw_item()
        for cell in equip_cells:
            cell.draw_item()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                for cell in loot_cells:
                    cell.check_for_input(event.pos)
                for cell in equip_cells:
                    cell.check_for_input(event.pos)

        if held_item is not None:
            screen.blit(held_item.image, pygame.mouse.get_pos())

        if keys[K_ESCAPE]:
            running = False
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()