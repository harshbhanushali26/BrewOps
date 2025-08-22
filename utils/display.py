from rich.console import Console, Group
from rich.table import Table
from rich import box
from rich.text import Text
from rich.panel import Panel
from rich.align import Align
from rich.padding import Padding
from rich.columns import Columns
from rich.rule import Rule


console = Console()
from datetime import date, datetime




def print_section_title(title, icon="📌", color="cyan"):
    console.print(f"\n[bold {color}]{icon} {title} [/bold {color}]\n")

# table format items listing
def display_menu_items(items: list, title="📋 Menu Items"):
    
    if not items:
        print_warning("No items found.")
        return

    table = Table(title=f"[bold white]{title}[/bold white]", show_header=True, header_style="bold magenta", box=box.SIMPLE_HEAVY)
    table.add_column("ID", style="bold cyan")
    table.add_column("Name", style="white")
    table.add_column("Category", style="magenta")
    table.add_column("Price (₹)", justify="right", style="green")
    table.add_column("Available", style="yellow")
    table.add_column("Special", style="bright_blue")

    for item in items:
        table.add_row(
            item.item_id,
            item.name,
            item.category,
            f"{item.price:.2f}",
            "✅" if item.available else "❌",
            "🌟" if item.is_special else "—"
        )

    console.print(table)


def print_header():
    console = Console()
    header_text = Align.center(Text("☕ BrewOps", style="bold bright_yellow"))

    panel = Panel(
        header_text,
        border_style="magenta",
        padding=(1, 2),
        title="System",
        title_align="center"
    )

    console.print(panel)


def print_success(message):
    console.print(f"\n✅ [green]{message}[/green]\n")


def print_warning(message):
    console.print(f"\n⚠️  [yellow]{message}[/yellow]\n")


def print_error(message):
    console.print(f"\n❌ [red]{message}[/red]\n")


def display_summary_panel(lines: list[str], title="📋 Summary", color="cyan"):
    group = Group(*[Text.from_markup(line) for line in lines])
    console.print(Panel.fit(group, title=title, border_style=color, padding=(1, 2)))


CATEGORY_EMOJIS = {
   "snacks": "🍟",
    "beverages": "🥤",
    "hot drinks": "☕",
    "cold drinks": "🧋 ",
    "desserts": "🍰 ",
    "sandwiches": "🥪",
    "pizza": "🍕 ",
    "burgers": "🍔",
    "combos": "🍽️ ",
    "breakfast": "🍳"
}


def get_category_emoji(category_name):
    return CATEGORY_EMOJIS.get(category_name.lower(), "📦")


def display_order_summary(order):
    # 🧾 Header
    header = Text.from_markup(f"[bold cyan]🧾 Order Summary[/bold cyan] - [green]{order.order_id}[/green]\n")
    
    # 📋 Table of Items
    table = Table(show_header=True, header_style="bold magenta", expand=False, box=None)
    table.add_column("Item", justify="left")
    table.add_column("Qty", justify="center")
    table.add_column("Price", justify="right")
    table.add_column("Total", justify="right")

    for item in order.items:
        name = item["name"]
        qty = item["qty"]
        price = item["price"]
        item_total = qty * price
        table.add_row(name, str(qty), f"₹{price:.2f}", f"₹{item_total:.2f}")

    # 📦 Footer info
    footer_lines = [
        f"\n[cyan]Total Amount:[/cyan] [bold green]₹{order.total_amount:.2f}[/bold green]",
        f"[cyan]Status:[/cyan] [yellow]{order.status.capitalize()}[/yellow]",
        f"[cyan]Paid:[/cyan] {'✅ Yes' if order.paid else '❌ No'}",
        f"[cyan]Date:[/cyan] {order.timestamp.split('T')[0]}"
    ]
    footer = Group(*[Text.from_markup(line) for line in footer_lines])

    group = Group(header, table, footer)
    panel = Panel(group, border_style="cyan", title="🍽️  Café Bill", expand=False)
    console.print(panel)


def display_view_menu(menu_manager):  # Menu for customers  

    available_items = {
        item.item_id: item for item in menu_manager.menu_items.values() if item.available
    }

    panels = []
    for category in menu_manager.categories:
        emoji = get_category_emoji(category)
        items_in_category = [
            item for item in available_items.values() if category == item.category
        ]

        if not items_in_category:
            continue

        items_str = ""
        for item in items_in_category:
            star = " ⭐" if item.is_special else ""
            name = f"{item.name}{star}"
            items_str += f"• {name:<26} ₹{item.price:>6}\n"

        panels.append(
            Panel.fit(
                items_str.strip(),
                title=f"{emoji} {category.upper()}",
                title_align="left",
                border_style="green",
                padding=(1, 2)
            )
        )

    # Group panels in chunks of 3
    def chunks(lst, n):
        for i in range(0, len(lst), n):
            yield lst[i:i + n]

    for panel_row in chunks(panels, 3):
        console.print(Columns(panel_row, equal=True, expand=True))


def display_multiple_orders_table(orders):
    if not orders:
        print_warning("No orders to display.")
        return
    
    
    table = Table(title=f"[bold white]📋 Orders Overview [/bold white]", show_header=True, header_style="bold magenta", box=box.SIMPLE_HEAVY)

    # table = Table(title="📋 Orders Overview")

    table.add_column("Order ID", style="cyan", no_wrap=True)
    table.add_column("Customer", style="bold white")
    table.add_column("Status", style="green")
    table.add_column("Paid", style="bold yellow")
    table.add_column("Total", style="bold white")
    table.add_column("Date", style="dim")

    for order in orders:
        paid_status = "✅ Yes" if order.paid else "❌ No"
        date_only = order.timestamp.split("T")[0] if "T" in order.timestamp else order.timestamp

        table.add_row(
            order.order_id,
            order.name or "-",
            order.status.capitalize(),
            paid_status,
            f"₹{order.total_amount:.2f}",
            date_only
        )

    console.print(table)


#========================== Menu (Options) =============================#

def admin_menu():   
    table = Table.grid(padding=(0, 2))
    table.add_column("Option", style="bold yellow")
    table.add_column("Action", style="white")

    table.add_row("1", "🍽️  Menu Management (Items & Categories)")
    table.add_row("2", "📦  Order Management")
    table.add_row("3", "📊  View Summary & Analytics")
    table.add_row("0", "🚪  Exit")
    
    console.print(Panel.fit(table, title="💻⚙️ Admin Portal", border_style="cyan", padding=(1, 2)))
   
   
def print_order_menu():
    
    table = Table.grid(padding=(0, 2))
    
    table.add_column("Option", justify="center", style="bold yellow")
    table.add_column("Action", style="bold white")

    table.add_row("1", "➕  Add Order")
    table.add_row("2", "✏️  Update Status")
    table.add_row("3", "🗑️  Mark Paid")
    table.add_row("4", "🔍  View Order")
    table.add_row("5", "📊  View All Orers")
    table.add_row("6", "🗑️  Remove Order")
    table.add_row("0", "🔙  Back")
    

    console.print(Panel.fit(table, title="📋 Order Management", border_style="cyan", padding=(1, 2)))
    
    
def analytics_menu():
    
    table = Table.grid(padding=(0, 2))
    
    table.add_column("Option", justify="center", style="bold yellow")
    table.add_column("Action", style="bold white")

    table.add_row("1", "📅  Daily Summary")
    table.add_row("2", "📆  Monthly Summary")
    table.add_row("3", "📊  Menu Insights")
    table.add_row("0", "🔙  Back")
    

    console.print(Panel.fit(table, title="📊 Analytics & Summary", border_style="cyan", padding=(1, 2)))


def customer_menu():
    
    console.print("\n[bold white]❓ What would you like to do?[/bold white]", style="cyan")
    table = Table.grid(padding=(0, 2))
    table.add_column("Option", style="bold yellow")
    table.add_column("Action", style="white")

    table.add_row("1", "📋  View Menu")
    table.add_row("2", "📝  Place Order")
    table.add_row("3", "👀  View Order")
    table.add_row("0", "🚪  Exit")
    
    console.print(Panel.fit(table, title="👤 Welcome to Cafe, Sir!!", border_style="green3", padding=(1, 2)))
       
#========================== Item & Category Menu (Options) =============================#   

def show_item_category_main_menu():
    
    table = Table.grid(padding=(0, 2))
    
    table.add_column("Option", justify="center", style="bold yellow")
    table.add_column("Action", style="bold white")

    table.add_row("1", "📚  Menu View & Filter")
    table.add_row("2", "🍽️  Manage Items")
    table.add_row("3", "🗂️  Manage Categories")
    table.add_row("0", "🔙  Back")
    
    console.print(Panel.fit(table, title="📋 Item & Category Management", border_style="cyan", padding=(1, 2)))
    
    
def manage_items_menu():

    table = Table.grid(padding=(0, 2))
    
    table.add_column("Option", justify="center", style="bold yellow")
    table.add_column("Action", style="bold white")

    table.add_row("1", "➕  Add Item")
    table.add_row("2", "✏️  Update Item")
    table.add_row("3", "🗑️  Remove Item")
    table.add_row("4", "🔄  Toggle Special")
    table.add_row("0", "🔙  Back")
    
    console.print(Panel.fit(table, title="🏷️ Manage Items", border_style="cyan", padding=(1, 2)))
    
    
def menu_views_summary_menu():

    table = Table.grid(padding=(0, 2))
    
    table.add_column("Option", justify="center", style="bold yellow")
    table.add_column("Action", style="bold white")

    table.add_row("1", "📋  View Menu")
    table.add_row("2", "🍽️  View Special Items")
    table.add_row("3", "🔍  Filter Menu Items")
    table.add_row("0", "🔙  Back")
    
    console.print(Panel.fit(table, title="📚 Menu View & Filter", border_style="cyan", padding=(1, 2)))
    
    
def manage_categories_menu():

    table = Table.grid(padding=(0, 2))
    
    table.add_column("Option", justify="center", style="bold yellow")
    table.add_column("Action", style="bold white")

    table.add_row("1", "➕  Add Category")
    table.add_row("2", "🗑️  Remove Category")
    table.add_row("0", "🔙  Back")
    
    console.print(Panel.fit(table, title="🗃️ Manage Categories", border_style="cyan", padding=(1, 2)))


# =========================== Summary ====================================#

def display_multiple_summary(summary: dict):
    
    if summary["total_orders"] == 0:
        print_warning("No sales for today!")
        return
    
    # ORDER AND REVENUE DETAILS
    order_lines = [
        # f"[cyan]Date:[/cyan] {target_date}",
        f" 🧾 [green]Total Orders:[/green] {summary["total_orders"]}",
        f" 💰 [green]Total Revenue:[/green] ₹{summary["total_revenue"]:.2f}",
        f" 📊 [green]Avg Order Value:[/green] ₹{summary["avg_order_value"]:.2f}"
    ]
    
    # TOP ORDERED ITEMS
    top_order_lines = []
    if summary["top_items"]:
        top_order_lines = [f"{name} — ordered [bold green]{count}[/bold green] times" for name, count in summary["top_items"]]
    else:
        print_warning("No top ordered items to show.")
        
    # LEAST ORDERED ITEMS
    least_order_lines = []
    if summary["least_items"]:
        least_order_lines = [f"{name} — ordered [bold red]{count}[/bold red] times (least)" for name, count in summary["least_items"]]
    else:
        print_warning("No least ordered items to show.")
        

    # 🏆 BEST CATEGORY BY ORDERS
    best_category_by_order_lines = []
    cat_orders = summary["best_category_by_orders"]
    if cat_orders:
        if isinstance(cat_orders, list):
            best_category_by_order_lines = [
                f"🏅 {name} — [bold cyan]{count}[/bold cyan] orders" for name, count in cat_orders
            ]
        else:
            name, count = cat_orders
            best_category_by_order_lines = [f"🏅 {name} — [bold cyan]{count}[/bold cyan] orders"]
    else:
        print_warning("No best category for order count to show.")

    # 💸 BEST CATEGORY BY REVENUE
    best_category_by_revenue_lines = []
    cat_revenue = summary["best_category_by_revenue"]
    if cat_revenue:
        if isinstance(cat_revenue, list):
            best_category_by_revenue_lines = [
                f"💰 {name} — ₹[bold yellow]{count:.2f}[/bold yellow] revenue" for name, count in cat_revenue
            ]
        else:
            name, count = cat_revenue
            best_category_by_revenue_lines = [f"💰 {name} — ₹[bold yellow]{count:.2f}[/bold yellow] revenue"]
    else:
        print_warning("No best category for revenue to show.")
        
    
    display_summary_panel(order_lines, "🧾 Order and Revenue", "magenta")
    display_summary_panel(top_order_lines, "🔝 Top Ordered Items", "green")
    display_summary_panel(least_order_lines, "🔻 Lowest Selling Items", "red")
    display_summary_panel(best_category_by_order_lines, "🏆 Best Category by Orders", "green")
    display_summary_panel(best_category_by_revenue_lines, "💸 Best Category by Revenue", "green")
        
        
def display_menu_summary(menu_summary):
    console.print(f"\n[green bold]ALL TIME[/green bold]\n")
    
    menu_lines = [
        f"🏷️ [green]Total Items:[/green] {menu_summary["total_items"]}",
        f"🗃️ [green]Total Categories:[/green] {menu_summary["total_categories"]}",
        f"📊 [green]Total Available Items:[/green] {menu_summary["available_count"]}",
        f"⭐ [green]Special Items:[/green] {menu_summary["special_count"]}"
    ]
    
    category_items_lines = []
    if menu_summary["category_wise_items"]:
        # number of items per category
        category_items_lines = [f"• {category.capitalize()} : [bold green]{count}[/bold green]" for category, count in menu_summary["category_wise_items"]]
    # number of orders per category
    category_order_lines = [f"• {cat.capitalize()} : [bold green]{qty}[/bold green] times ordered" for cat, qty in menu_summary["category_wise_orders"]]
    
    display_summary_panel(menu_lines, "🍽️ Menu Summary")
    display_summary_panel(category_items_lines, "📂 Items by Category", "magenta")
    display_summary_panel(category_order_lines, "📦 Orders per Category", "yellow")
    
    
# ========================================== Dashboard =========================================== #   
    
def get_today_panel(today_summary):
        today_panel = Panel.fit(
        f"""📅 [bold magenta]Today: {date.today()}[/bold magenta]
├─ Total Orders Today: [bold green]{today_summary['total_orders']}[/bold green]
├─ Total Revenue Today: [bold green]₹{today_summary['total_revenue']:.2f}[/bold green]
├─ Avg. Order Value: [bold green]₹{today_summary['avg_order_value']:.2f}[/bold green]
├─ Top Item Today: {today_summary['top_item']}
└─ Peak Hour Today: [bold yellow]{today_summary['peak_hour']}[/bold yellow]
        """,
        title=f"📊 Welcome back, Admin!",
        border_style="cyan",
        padding=(1, 2)
    )
        return today_panel   
    
    
def get_monthly_panel(month_summary):
        month_panel = Panel.fit(
        f"""🗓️  [bold magenta]This Month: {date.today():%B %Y}[/bold magenta]
├─ Orders This Month: [bold green]{month_summary['total_orders']}[/bold green]
├─ Revenue This Month: [bold green]₹{month_summary['total_revenue']:.2f}[/bold green]
├─ Avg. Daily Revenue: [bold green]₹{month_summary['avg_order_value']:.2f}[/bold green]
├─ Best Selling Item: {month_summary['top_item']}
├─ Low Performing Item 1: {month_summary['least_item']}
└─ Low Performing Items 2: {month_summary['second_least_item']}
        """,
        title = "Monthly Summary",
        border_style="green",
        padding=(1, 2)
    )
        return month_panel


def get_category_panel(menu_summary):
    menu_panel = Panel.fit(
        f"""
├─ Total Items: [bold green]{menu_summary["total_items"]}[/bold green]
├─ Total Categories: [bold green]{menu_summary["total_categories"]}[/bold green]
├─ Available Items: [bold green]{menu_summary["available_count"]}[/bold green]
└─ Special Items: [bold green]{menu_summary["special_count"]}[/bold green]
        """,
        title="🍽️ Menu Summary",
        border_style="yellow",
        padding=(1, 2)
        )
    
    # Create table version (more structured)
    category_table = Table(show_header=True, header_style="bold red", box=box.SIMPLE)
    category_table.add_column("🍽️ Category", justify="left")
    category_table.add_column("📦 Items Order", justify="right")
    category_table.add_column("📊 Percentage", justify="right")
    
    # Calculate total orders for percentage
    total_orders = sum(qty for cat, qty in menu_summary["category_wise_orders"])
    
    # Sort by quantity (highest first)
    sorted_categories = sorted(menu_summary["category_wise_orders"], key=lambda x: x[1], reverse=True)
    
    for category, quantity in sorted_categories:
        percentage = (quantity / total_orders * 100) if total_orders > 0 else 0
        category_table.add_row(
            category.capitalize(),
            f"[bold green]{quantity}[/bold green]",
            f"{percentage:.1f}%"
        )
    
    # Add total row
    category_table.add_row("", "", "", style="dim")
    category_table.add_row(
        "[bold]TOTAL[/bold]",
        f"[bold]{total_orders}[/bold]",
        "[bold]100.0%[/bold]"
    )
    
    category_panel = Panel.fit(
        category_table,
        title="📊 [bold red]📦 Orders Per Category[/bold red]",
        border_style="red",
        padding=(1, 2)
    )
    
    summary_panel = Columns([menu_panel, category_panel], align="center", equal=True, expand=True)

    
    return summary_panel
        

def get_weekly_sales_panel(weekly_data):
    """
    Creates a Rich panel displaying weekly sales details from get_weekly_sales_details()
    
    Args:
        weekly_data: Dictionary returned from get_weekly_sales_details() containing
                    daily_avg, total_revenue, and weekly_summary
    """
    
    # Create main table for daily breakdown
    weekly_table = Table(show_header=True, header_style="bold magenta", box=box.SIMPLE)
    weekly_table.add_column("📅 Date", justify="left")
    weekly_table.add_column("🗓️ Day", justify="left") 
    weekly_table.add_column("📦 Orders", justify="right")
    weekly_table.add_column("💰 Revenue", justify="right")
    
    # Add rows for each day (reverse to show most recent first)
    for day_data in reversed(weekly_data["weekly_summary"]):
        weekly_table.add_row(
            day_data["date"],
            day_data["weekday"],
            str(day_data["per_day_orders"]),
            f"₹{day_data['per_day_revenue']:.2f}"
        )
    
    # Add separator and summary rows
    weekly_table.add_row("", "", "", "", style="dim")
    weekly_table.add_row(
        "[bold]TOTAL[/bold]", 
        "[bold]7 Days[/bold]", 
        f"[bold]{sum(day['per_day_orders'] for day in weekly_data['weekly_summary'])}[/bold]",
        f"[bold green]₹{weekly_data['total_revenue']:.2f}[/bold green]"
    )
    weekly_table.add_row(
        "[bold]DAILY AVG[/bold]", 
        "[bold]Per Day[/bold]", 
        f"[bold]{sum(day['per_day_orders'] for day in weekly_data['weekly_summary']) / 7:.1f}[/bold]",
        f"[bold green]₹{weekly_data['daily_avg']:.2f}[/bold green]"
    )

    # Create panel
    weekly_panel = Panel.fit(
        weekly_table,
        title="📈 Last 7 Days Sales Summary",
        border_style="green",
        padding=(1, 2)
    )
    
    return weekly_panel

    
def display_dashboard(today_summary, month_summary, menu_summary, weekly_insights):
    today_panel = get_today_panel(today_summary)
    month_panel = get_monthly_panel(month_summary)
    category_panel =  get_category_panel(menu_summary)
    weekly_panel = get_weekly_sales_panel(weekly_insights)
 
    row_1 = Columns([today_panel, month_panel, weekly_panel],align="center", equal=True, expand=True)
    row_2 = Columns([category_panel], align="center",  equal=True, expand=True)

    dashboard = Panel(
        Group(row_1,Rule(style="dim"), row_2),
        title="📊 Cafe Management Dashboard",
        border_style="bold blue",
        padding=(1, 2)
    )
    
    console.print(dashboard)
        
    

# 📈 Last 7 Days Sales
# 29 Jul (Tue)  ₹3,120   (26 Orders)
# 28 Jul (Mon)  ₹2,340   (22 Orders)
# 27 Jul (Sun)  ₹3,790   (34 Orders)
# 26 Jul (Sat)  ₹4,110   (37 Orders)
# 25 Jul (Fri)  ₹3,520   (31 Orders)
# 24 Jul (Thu)  ₹2,680   (23 Orders)
# 23 Jul (Wed)  ₹1,870   (17 Orders)

# 📊 Total: ₹21,430 | Daily Avg: ₹3,061


    # add live or as of 15:30 for today in progress
    # after 23:00 time remove live to show as full data 


# (optional)
# 💡 Suggestions
# • Items to Promote: [Garlic Bread, Iced Tea]
# • Inventory Alerts: [Paneer, Coffee Beans]

# 📌 System Stats
# • Last Backup        : Today at 3:30 PM
# • System Version     : v1.3.2
# • Users Logged In    : 1 (Admin)
