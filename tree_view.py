import os

def print_tree(start_path='.', prefix=''):
    """
    Рекурсивно виводить дерево файлів і папок у стилі Linux tree
    """
    # Отримуємо всі елементи (сортуємо, щоб директорії були першими)
    entries = sorted(os.listdir(start_path), key=lambda x: (not os.path.isdir(os.path.join(start_path, x)), x.lower()))
    entries_count = len(entries)
    
    for i, name in enumerate(entries):
        path = os.path.join(start_path, name)
        connector = "└── " if i == entries_count - 1 else "├── "
        print(prefix + connector + name)
        if os.path.isdir(path):
            extension = "    " if i == entries_count - 1 else "│   "
            print_tree(path, prefix + extension)

if __name__ == "__main__":
    root_dir = "app"  # коренева папка твого проєкту
    print(f"\n📁 Структура проєкту '{root_dir}':\n")
    print_tree(root_dir)
