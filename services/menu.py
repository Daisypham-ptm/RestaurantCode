from menu import Category


def main():
    print("=== MENU TEST ===\n")

    
    category = Category(
        category_id=1,
        category_name="Food",
        description="Food Menu"
    )

    items = category.get_menu_items()

    if not items:
        print(" Không có món nào trong danh mục này")
        return

    print(f"Danh sách món trong category '{category.category_name}':\n")

    for item in items:
        print(f"- ID: {item.item_id}")
        print(f"  Tên: {item.item_name}")
        print(f"  Mô tả: {item.description}")
        print(f"  Giá: {item.price}")
        print(f"  Trạng thái: {item.status}")
        print(f"  Rating TB: {item.avg_rating}")
        print("-" * 30)


if __name__ == "__main__":
    main()
