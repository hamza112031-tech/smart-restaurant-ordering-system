import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv
import os
import sys

# ─── Make sure hamza.py is importable from same directory ───────────────────
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# ─── Colours & Fonts ────────────────────────────────────────────────────────
BG          = "#1A1A2E"   # deep navy
SURFACE     = "#16213E"   # card bg
ACCENT      = "#E94560"   # crimson‑red
GOLD        = "#F5A623"   # warm gold
TEXT        = "#EAEAEA"   # near‑white
SUBTEXT     = "#A0A0B0"   # muted
GREEN       = "#2ECC71"
FONT_TITLE  = ("Georgia", 22, "bold")
FONT_HEAD   = ("Georgia", 14, "bold")
FONT_BODY   = ("Helvetica", 11)
FONT_SMALL  = ("Helvetica", 9)
FONT_BTN    = ("Helvetica", 11, "bold")

PREPARATION_TIMES = {
    "Koshari Medium": 10, "Grilled Chicken Meal": 25,
    "Shish Tawook Sandwich": 15, "Beef Burger Combo": 20,
    "Margherita Pizza Medium": 18, "Fatteh with Chicken": 22,
    "Fried Shrimp Plate": 15, "Caesar Salad": 8,
    "Chicken Pasta Alfredo": 20, "Molokhia with Rice and Chicken": 30,
}

MENU_FILE    = os.path.join(os.path.dirname(os.path.abspath(__file__)), "menu2.txt")
ORDERS_FILE  = os.path.join(os.path.dirname(os.path.abspath(__file__)), "saved_orders.txt")
CLIENTS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "menu_from_clients.txt")


# ─── Helpers ────────────────────────────────────────────────────────────────
def load_menu():
    menu = {}
    try:
        with open(MENU_FILE, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if "-" in line:
                    parts = line.split("-", 1)
                    try:
                        menu[parts[0].strip()] = float(parts[1].strip())
                    except ValueError:
                        pass
    except FileNotFoundError:
        pass
    return menu


def load_saved_orders():
    all_orders = []
    current = {}
    try:
        with open(ORDERS_FILE, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line == "New Order:":
                    current = {}
                elif line.startswith("-"):
                    if current:
                        all_orders.append(current)
                elif "x" in line and "=" in line:
                    try:
                        item, rest = line.split("x", 1)
                        qty = int(rest.split("=")[0].strip())
                        current[item.strip()] = qty
                    except Exception:
                        pass
    except FileNotFoundError:
        pass
    return all_orders


def save_order_to_file(orders, menu):
    with open(ORDERS_FILE, "a", encoding="utf-8") as f:
        f.write("New Order:\n")
        for item, qty in orders.items():
            total = menu[item] * qty
            f.write(f"{item} x{qty} = {total}\n")
        f.write("-" * 30 + "\n")


# ─── Styled Widgets ──────────────────────────────────────────────────────────
def styled_btn(parent, text, cmd, color=ACCENT, width=20):
    return tk.Button(
        parent, text=text, command=cmd,
        bg=color, fg="white", font=FONT_BTN,
        relief="flat", cursor="hand2", width=width,
        activebackground=GOLD, activeforeground=BG,
        pady=6
    )


def card_frame(parent, **kw):
    return tk.Frame(parent, bg=SURFACE, bd=0, relief="flat", **kw)


# ════════════════════════════════════════════════════════════════════════════
#  MAIN APPLICATION
# ════════════════════════════════════════════════════════════════════════════
class RestaurantApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("🍽  Luxurious Restaurant")
        self.geometry("1050x680")
        self.resizable(True, True)
        self.configure(bg=BG)
        self._show_home()

    # ── routing ──────────────────────────────────────────────────────────────
    def _clear(self):
        for w in self.winfo_children():
            w.destroy()

    def _show_home(self):
        self._clear()
        HomeScreen(self)

    def _show_customer(self):
        self._clear()
        CustomerScreen(self)

    def _show_agent(self):
        self._clear()
        AgentLoginScreen(self)


# ════════════════════════════════════════════════════════════════════════════
#  HOME SCREEN
# ════════════════════════════════════════════════════════════════════════════
class HomeScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=BG)
        self.pack(fill="both", expand=True)

        # top decorative bar
        bar = tk.Frame(self, bg=ACCENT, height=6)
        bar.pack(fill="x")

        # centre content
        centre = tk.Frame(self, bg=BG)
        centre.place(relx=0.5, rely=0.45, anchor="center")

        tk.Label(centre, text="🍽", font=("Helvetica", 52), bg=BG, fg=GOLD).pack()
        tk.Label(centre, text="LUXURIOUS RESTAURANT",
                 font=("Georgia", 28, "bold"), bg=BG, fg=TEXT).pack(pady=(6, 2))
        tk.Label(centre, text="Your destination for exquisite dining",
                 font=("Helvetica", 12, "italic"), bg=BG, fg=SUBTEXT).pack(pady=(0, 30))

        btn_frame = tk.Frame(centre, bg=BG)
        btn_frame.pack()
        styled_btn(btn_frame, "👤  Customer Access", master._show_customer,
                   color=ACCENT, width=22).grid(row=0, column=0, padx=12, pady=8)
        styled_btn(btn_frame, "🔑  Agent Login", master._show_agent,
                   color="#2C3E7A", width=22).grid(row=0, column=1, padx=12, pady=8)

        tk.Label(self, text="© 2025 Luxurious Restaurant — All Rights Reserved",
                 font=FONT_SMALL, bg=BG, fg=SUBTEXT).pack(side="bottom", pady=8)


# ════════════════════════════════════════════════════════════════════════════
#  CUSTOMER SCREEN
# ════════════════════════════════════════════════════════════════════════════
class CustomerScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=BG)
        self.pack(fill="both", expand=True)
        self.master = master
        self.menu = load_menu()
        self.cart = {}       # item -> qty

        self._build_layout()

    # ── layout ───────────────────────────────────────────────────────────────
    def _build_layout(self):
        # header
        hdr = tk.Frame(self, bg=ACCENT, pady=10)
        hdr.pack(fill="x")
        tk.Label(hdr, text="🍽  Customer Menu", font=FONT_TITLE,
                 bg=ACCENT, fg="white").pack(side="left", padx=20)
        styled_btn(hdr, "← Back", self.master._show_home,
                   color="#222244", width=10).pack(side="right", padx=14)

        # body: left = menu, right = cart+actions
        body = tk.Frame(self, bg=BG)
        body.pack(fill="both", expand=True, padx=16, pady=12)
        body.columnconfigure(0, weight=3)
        body.columnconfigure(1, weight=2)
        body.rowconfigure(0, weight=1)

        self._build_menu_panel(body)
        self._build_right_panel(body)

    def _build_menu_panel(self, parent):
        left = card_frame(parent)
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 8))

        tk.Label(left, text="Available Items", font=FONT_HEAD,
                 bg=SURFACE, fg=GOLD).pack(anchor="w", padx=12, pady=(10, 4))

        # search bar
        sf = tk.Frame(left, bg=SURFACE)
        sf.pack(fill="x", padx=12, pady=(0, 8))
        self.search_var = tk.StringVar()
        self.search_var.trace("w", self._filter_menu)
        tk.Entry(sf, textvariable=self.search_var, font=FONT_BODY,
                 bg="#0F3460", fg=TEXT, insertbackground=TEXT,
                 relief="flat", bd=6).pack(fill="x")

        # menu list
        cols = ("Item", "Price (EGP)")
        self.menu_tree = ttk.Treeview(left, columns=cols, show="headings", height=18)
        self._style_tree(self.menu_tree)
        for c in cols:
            self.menu_tree.heading(c, text=c)
            self.menu_tree.column(c, anchor="w")
        self.menu_tree.column("Price (EGP)", anchor="center", width=110)
        self.menu_tree.pack(fill="both", expand=True, padx=12, pady=(0, 4))

        btn_row = tk.Frame(left, bg=SURFACE)
        btn_row.pack(padx=12, pady=8)
        styled_btn(btn_row, "➕ Add to Cart", self._add_to_cart,
                   color=GREEN, width=16).pack(side="left", padx=4)
        styled_btn(btn_row, "📋 Best Seller", self._show_best_seller,
                   color="#8E44AD", width=16).pack(side="left", padx=4)

        self._populate_menu(self.menu)

    def _build_right_panel(self, parent):
        right = card_frame(parent)
        right.grid(row=0, column=1, sticky="nsew")

        # ── cart ──
        tk.Label(right, text="🛒 Your Cart", font=FONT_HEAD,
                 bg=SURFACE, fg=GOLD).pack(anchor="w", padx=12, pady=(10, 4))

        cart_cols = ("Item", "Qty", "Subtotal")
        self.cart_tree = ttk.Treeview(right, columns=cart_cols, show="headings", height=9)
        self._style_tree(self.cart_tree)
        for c in cart_cols:
            self.cart_tree.heading(c, text=c)
        self.cart_tree.column("Item", width=140)
        self.cart_tree.column("Qty", width=40, anchor="center")
        self.cart_tree.column("Subtotal", width=80, anchor="center")
        self.cart_tree.pack(fill="x", padx=12)

        self.total_lbl = tk.Label(right, text="Total: 0 EGP",
                                  font=("Helvetica", 12, "bold"),
                                  bg=SURFACE, fg=GOLD)
        self.total_lbl.pack(anchor="e", padx=16, pady=4)

        btn_f = tk.Frame(right, bg=SURFACE)
        btn_f.pack(padx=12, pady=4, fill="x")
        styled_btn(btn_f, "🗑 Remove Item", self._remove_from_cart,
                   color="#C0392B", width=16).pack(side="left", padx=2)
        styled_btn(btn_f, "✅ Place Order", self._place_order,
                   color=ACCENT, width=16).pack(side="left", padx=2)

        # ── discount ──
        sep = tk.Frame(right, bg=ACCENT, height=2)
        sep.pack(fill="x", padx=12, pady=8)

        tk.Label(right, text="🎁 Discount", font=FONT_HEAD,
                 bg=SURFACE, fg=GOLD).pack(anchor="w", padx=12)

        disc_f = tk.Frame(right, bg=SURFACE)
        disc_f.pack(padx=12, pady=6, fill="x")
        tk.Label(disc_f, text="Code:", font=FONT_BODY,
                 bg=SURFACE, fg=TEXT).pack(side="left")
        self.disc_entry = tk.Entry(disc_f, width=8, font=FONT_BODY,
                                   bg="#0F3460", fg=TEXT, insertbackground=TEXT, relief="flat", bd=4)
        self.disc_entry.pack(side="left", padx=6)
        styled_btn(disc_f, "Apply", self._apply_discount,
                   color="#2C3E7A", width=8).pack(side="left")

        self.disc_lbl = tk.Label(right, text="", font=FONT_BODY, bg=SURFACE, fg=GREEN)
        self.disc_lbl.pack(anchor="w", padx=12)

        # ── tables ──
        sep2 = tk.Frame(right, bg=ACCENT, height=2)
        sep2.pack(fill="x", padx=12, pady=8)

        tk.Label(right, text="🪑 Available Tables", font=FONT_HEAD,
                 bg=SURFACE, fg=GOLD).pack(anchor="w", padx=12)

        tables_f = tk.Frame(right, bg=SURFACE)
        tables_f.pack(padx=12, pady=6, fill="x")
        all_tables = {**{f"table_{i}": False for i in range(1, 16)},
                      **{f"vip_{i}": False for i in range(1, 6)}}
        available = [t for t, r in all_tables.items() if not r]
        tk.Label(tables_f, text=f"{len(available)} tables free  (15 regular + 5 VIP)",
                 font=FONT_BODY, bg=SURFACE, fg=TEXT).pack(anchor="w")

    # ── helpers ──────────────────────────────────────────────────────────────
    def _style_tree(self, tree):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background=BG, foreground=TEXT,
                        fieldbackground=BG, font=FONT_BODY, rowheight=26)
        style.configure("Treeview.Heading", background=SURFACE,
                        foreground=GOLD, font=("Helvetica", 10, "bold"))
        style.map("Treeview", background=[("selected", ACCENT)])

    def _populate_menu(self, items):
        self.menu_tree.delete(*self.menu_tree.get_children())
        for item, price in items.items():
            self.menu_tree.insert("", "end", values=(item, f"{price:.2f}"))

    def _filter_menu(self, *_):
        kw = self.search_var.get().lower()
        filtered = {k: v for k, v in self.menu.items() if kw in k.lower()}
        self._populate_menu(filtered)

    def _add_to_cart(self):
        sel = self.menu_tree.selection()
        if not sel:
            messagebox.showwarning("Select Item", "Please select an item from the menu first.")
            return
        item_name = self.menu_tree.item(sel[0])["values"][0]

        # qty dialog
        dlg = tk.Toplevel(self)
        dlg.title("Quantity")
        dlg.configure(bg=BG)
        dlg.resizable(False, False)
        dlg.grab_set()
        tk.Label(dlg, text=f"How many  {item_name}?",
                 font=FONT_BODY, bg=BG, fg=TEXT).pack(padx=20, pady=(14, 4))
        qty_var = tk.IntVar(value=1)
        tk.Spinbox(dlg, from_=1, to=20, textvariable=qty_var,
                   font=FONT_BODY, width=6, bg=SURFACE, fg=TEXT).pack(pady=4)

        def confirm():
            qty = qty_var.get()
            if item_name in self.cart:
                self.cart[item_name] += qty
            else:
                self.cart[item_name] = qty
            self._refresh_cart()
            dlg.destroy()

        styled_btn(dlg, "Add", confirm, color=GREEN, width=10).pack(pady=10)

    def _remove_from_cart(self):
        sel = self.cart_tree.selection()
        if not sel:
            return
        item_name = self.cart_tree.item(sel[0])["values"][0]
        del self.cart[item_name]
        self._refresh_cart()

    def _refresh_cart(self):
        self.cart_tree.delete(*self.cart_tree.get_children())
        total = 0
        for item, qty in self.cart.items():
            subtotal = self.menu.get(item, 0) * qty
            total += subtotal
            self.cart_tree.insert("", "end", values=(item, qty, f"{subtotal:.2f}"))
        self.total_lbl.config(text=f"Total: {total:.2f} EGP")

    def _place_order(self):
        if not self.cart:
            messagebox.showwarning("Empty Cart", "Your cart is empty!")
            return
        save_order_to_file(self.cart, self.menu)
        total = sum(self.menu[i] * q for i, q in self.cart.items())
        prep  = sum(PREPARATION_TIMES.get(i, 10) * q for i, q in self.cart.items())
        messagebox.showinfo("Order Placed ✅",
                            f"Order saved successfully!\n\n"
                            f"Total: {total:.2f} EGP\n"
                            f"Est. preparation time: ~{prep} min")
        self.cart.clear()
        self._refresh_cart()

    def _apply_discount(self):
        codes = {7: 0.35, 11: 0.22, 22: 0.15, 33: 0.10, 44: 0.20}
        raw = self.disc_entry.get().strip()
        # check first-visit
        if raw.lower() == "first":
            pct = 30
        else:
            try:
                code = int(raw)
            except ValueError:
                messagebox.showerror("Invalid", "Enter a numeric code or 'first'")
                return
            if code not in codes:
                messagebox.showinfo("No Discount", "Code not recognised.")
                self.disc_lbl.config(text="")
                return
            pct = int(codes[code] * 100)
        self.disc_lbl.config(text=f"🎉 {pct}% discount applied!")

    def _show_best_seller(self):
        sales = {}
        try:
            with open(ORDERS_FILE, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if "x" in line and "=" in line:
                        try:
                            item, rest = line.split("x", 1)
                            qty = int(rest.split("=")[0].strip())
                            sales[item.strip()] = sales.get(item.strip(), 0) + qty
                        except Exception:
                            pass
        except FileNotFoundError:
            pass
        if not sales:
            messagebox.showinfo("Best Seller", "No orders recorded yet.")
            return
        best = max(sales, key=sales.get)
        messagebox.showinfo("🏆 Best Seller",
                            f"Best selling item:\n\n{best}\n({sales[best]} orders)")


# ════════════════════════════════════════════════════════════════════════════
#  AGENT LOGIN
# ════════════════════════════════════════════════════════════════════════════
class AgentLoginScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=BG)
        self.pack(fill="both", expand=True)
        self.master = master

        centre = tk.Frame(self, bg=SURFACE, padx=40, pady=36)
        centre.place(relx=0.5, rely=0.45, anchor="center")

        tk.Label(centre, text="🔑  Agent Login", font=FONT_TITLE,
                 bg=SURFACE, fg=GOLD).pack(pady=(0, 20))
        tk.Label(centre, text="Password", font=FONT_BODY,
                 bg=SURFACE, fg=TEXT).pack(anchor="w")
        self.pw = tk.Entry(centre, show="●", font=FONT_BODY, width=22,
                           bg=BG, fg=TEXT, insertbackground=TEXT, relief="flat", bd=6)
        self.pw.pack(pady=6)
        self.pw.bind("<Return>", lambda _: self._login())

        btn_row = tk.Frame(centre, bg=SURFACE)
        btn_row.pack(pady=12)
        styled_btn(btn_row, "Login", self._login, color=ACCENT, width=12).pack(side="left", padx=6)
        styled_btn(btn_row, "← Back", master._show_home, color="#444466", width=12).pack(side="left", padx=6)

    def _login(self):
        if self.pw.get() == "2025":
            self.master._clear()
            AgentScreen(self.master)
        else:
            messagebox.showerror("Access Denied", "Wrong password!")


# ════════════════════════════════════════════════════════════════════════════
#  AGENT SCREEN
# ════════════════════════════════════════════════════════════════════════════
class AgentScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=BG)
        self.pack(fill="both", expand=True)
        self.master = master
        self.menu = load_menu()

        # header
        hdr = tk.Frame(self, bg="#2C3E7A", pady=10)
        hdr.pack(fill="x")
        tk.Label(hdr, text="🔑  Agent Dashboard", font=FONT_TITLE,
                 bg="#2C3E7A", fg="white").pack(side="left", padx=20)
        styled_btn(hdr, "← Logout", master._show_home,
                   color=ACCENT, width=10).pack(side="right", padx=14)

        # tabs
        nb = ttk.Notebook(self)
        nb.pack(fill="both", expand=True, padx=14, pady=10)
        self._style_notebook(nb)

        tab1 = tk.Frame(nb, bg=BG)
        tab2 = tk.Frame(nb, bg=BG)
        tab3 = tk.Frame(nb, bg=BG)
        tab4 = tk.Frame(nb, bg=BG)

        nb.add(tab1, text="  📋 Menu Manager  ")
        nb.add(tab2, text="  📦 Orders & Report  ")
        nb.add(tab3, text="  📊 Export CSV  ")
        nb.add(tab4, text="  👤 Register Customer  ")

        self._build_menu_tab(tab1)
        self._build_orders_tab(tab2)
        self._build_export_tab(tab3)
        self._build_register_tab(tab4)

    def _style_notebook(self, nb):
        s = ttk.Style()
        s.theme_use("clam")
        s.configure("TNotebook", background=BG, borderwidth=0)
        s.configure("TNotebook.Tab", background=SURFACE, foreground=TEXT,
                    font=FONT_BODY, padding=[12, 6])
        s.map("TNotebook.Tab", background=[("selected", ACCENT)],
              foreground=[("selected", "white")])

    # ── Menu Manager tab ─────────────────────────────────────────────────────
    def _build_menu_tab(self, parent):
        left = card_frame(parent, padx=12, pady=10)
        left.pack(side="left", fill="both", expand=True, padx=(10, 5), pady=10)
        right = card_frame(parent, padx=12, pady=10)
        right.pack(side="right", fill="y", padx=(5, 10), pady=10)

        tk.Label(left, text="Current Menu", font=FONT_HEAD, bg=SURFACE, fg=GOLD).pack(anchor="w")
        cols = ("Item", "Price")
        self.menu_mgr_tree = ttk.Treeview(left, columns=cols, show="headings", height=18)
        for c in cols:
            self.menu_mgr_tree.heading(c, text=c)
        self.menu_mgr_tree.column("Price", width=100, anchor="center")
        self.menu_mgr_tree.pack(fill="both", expand=True, pady=6)
        self._reload_menu_tree()

        # right: add / remove
        tk.Label(right, text="Add Item", font=FONT_HEAD, bg=SURFACE, fg=GOLD).pack(anchor="w", pady=(0, 6))
        tk.Label(right, text="Item name:", font=FONT_BODY, bg=SURFACE, fg=TEXT).pack(anchor="w")
        self.new_item_var = tk.StringVar()
        tk.Entry(right, textvariable=self.new_item_var, width=22, font=FONT_BODY,
                 bg=BG, fg=TEXT, insertbackground=TEXT, relief="flat", bd=5).pack(pady=3)
        tk.Label(right, text="Price (EGP):", font=FONT_BODY, bg=SURFACE, fg=TEXT).pack(anchor="w")
        self.new_price_var = tk.StringVar()
        tk.Entry(right, textvariable=self.new_price_var, width=22, font=FONT_BODY,
                 bg=BG, fg=TEXT, insertbackground=TEXT, relief="flat", bd=5).pack(pady=3)
        styled_btn(right, "➕ Add Item", self._add_item, color=GREEN, width=18).pack(pady=10)

        tk.Frame(right, bg=ACCENT, height=2, width=180).pack(fill="x", pady=10)
        tk.Label(right, text="Remove Item", font=FONT_HEAD, bg=SURFACE, fg=GOLD).pack(anchor="w")
        tk.Label(right, text="Select from list then click:", font=FONT_SMALL,
                 bg=SURFACE, fg=SUBTEXT).pack(anchor="w")
        styled_btn(right, "🗑 Remove Selected", self._remove_item, color="#C0392B", width=18).pack(pady=8)

    def _reload_menu_tree(self):
        self.menu = load_menu()
        self.menu_mgr_tree.delete(*self.menu_mgr_tree.get_children())
        for item, price in self.menu.items():
            self.menu_mgr_tree.insert("", "end", values=(item, f"{price:.2f}"))

    def _add_item(self):
        name = self.new_item_var.get().strip()
        price_s = self.new_price_var.get().strip()
        if not name or not price_s:
            messagebox.showwarning("Missing", "Enter both name and price.")
            return
        try:
            price = float(price_s)
        except ValueError:
            messagebox.showerror("Error", "Price must be a number.")
            return
        with open(MENU_FILE, "a", encoding="utf-8") as f:
            f.write(f"\n{name}-{price}")
        messagebox.showinfo("Added", f"'{name}' added successfully!")
        self.new_item_var.set("")
        self.new_price_var.set("")
        self._reload_menu_tree()

    def _remove_item(self):
        sel = self.menu_mgr_tree.selection()
        if not sel:
            messagebox.showwarning("Select", "Select an item to remove.")
            return
        item_name = self.menu_mgr_tree.item(sel[0])["values"][0]
        if not messagebox.askyesno("Confirm", f"Remove '{item_name}'?"):
            return
        with open(MENU_FILE, "r", encoding="utf-8") as f:
            lines = f.readlines()
        with open(MENU_FILE, "w", encoding="utf-8") as f:
            for line in lines:
                if "-" in line and line.split("-")[0].strip().lower() != item_name.lower():
                    f.write(line)
        messagebox.showinfo("Removed", f"'{item_name}' removed.")
        self._reload_menu_tree()

    # ── Orders & Report tab ──────────────────────────────────────────────────
    def _build_orders_tab(self, parent):
        top = card_frame(parent, padx=12, pady=10)
        top.pack(fill="both", expand=True, padx=10, pady=10)

        hdr = tk.Frame(top, bg=SURFACE)
        hdr.pack(fill="x")
        tk.Label(hdr, text="Orders & Daily Report", font=FONT_HEAD,
                 bg=SURFACE, fg=GOLD).pack(side="left")
        styled_btn(hdr, "🔄 Refresh", self._load_report, color="#2C3E7A", width=10).pack(side="right", pady=4)

        cols = ("Item", "Qty Sold", "Revenue (EGP)")
        self.report_tree = ttk.Treeview(top, columns=cols, show="headings", height=16)
        for c in cols:
            self.report_tree.heading(c, text=c)
        self.report_tree.column("Qty Sold", width=100, anchor="center")
        self.report_tree.column("Revenue (EGP)", width=130, anchor="center")
        self.report_tree.pack(fill="both", expand=True, pady=8)

        self.report_total_lbl = tk.Label(top, text="", font=("Helvetica", 12, "bold"),
                                         bg=SURFACE, fg=GOLD)
        self.report_total_lbl.pack(anchor="e", padx=10)
        self._load_report()

    def _load_report(self):
        self.menu = load_menu()
        all_orders = load_saved_orders()
        report = {}
        for order in all_orders:
            for item, qty in order.items():
                if item in self.menu:
                    if item not in report:
                        report[item] = {"qty": qty, "rev": qty * self.menu[item]}
                    else:
                        report[item]["qty"] += qty
                        report[item]["rev"] += qty * self.menu[item]
        self.report_tree.delete(*self.report_tree.get_children())
        grand = 0
        for item, d in report.items():
            self.report_tree.insert("", "end", values=(item, d["qty"], f"{d['rev']:.2f}"))
            grand += d["rev"]
        self.report_total_lbl.config(text=f"Grand Total Revenue: {grand:.2f} EGP")

    # ── Export CSV tab ───────────────────────────────────────────────────────
    def _build_export_tab(self, parent):
        centre = card_frame(parent, padx=20, pady=20)
        centre.place(relx=0.5, rely=0.45, anchor="center", width=480)

        tk.Label(centre, text="Export Daily Sales to CSV", font=FONT_HEAD,
                 bg=SURFACE, fg=GOLD).pack(pady=(0, 14))

        self.export_items = {}
        frame = tk.Frame(centre, bg=SURFACE)
        frame.pack(fill="x")

        tk.Label(frame, text="Item Name", font=FONT_BODY, bg=SURFACE, fg=TEXT,
                 width=22, anchor="w").grid(row=0, column=0)
        tk.Label(frame, text="Qty Sold", font=FONT_BODY, bg=SURFACE, fg=TEXT,
                 width=10, anchor="w").grid(row=0, column=1)

        self.exp_name = tk.Entry(frame, font=FONT_BODY, width=22,
                                 bg=BG, fg=TEXT, insertbackground=TEXT, relief="flat", bd=4)
        self.exp_name.grid(row=1, column=0, pady=4, padx=2)
        self.exp_qty = tk.Entry(frame, font=FONT_BODY, width=10,
                                bg=BG, fg=TEXT, insertbackground=TEXT, relief="flat", bd=4)
        self.exp_qty.grid(row=1, column=1, pady=4, padx=2)

        tk.Label(centre, text="(from saved orders)", font=FONT_SMALL, bg=SURFACE, fg=SUBTEXT).pack()
        styled_btn(centre, "📊 Export from Orders", self._export_from_orders,
                   color=ACCENT, width=24).pack(pady=10)

    def _export_from_orders(self):
        all_orders = load_saved_orders()
        if not all_orders:
            messagebox.showinfo("No Data", "No saved orders to export.")
            return
        sales = {}
        for order in all_orders:
            for item, qty in order.items():
                sales[item] = sales.get(item, 0) + qty
        path = filedialog.asksaveasfilename(
            defaultextension=".csv", filetypes=[("CSV files", "*.csv")],
            title="Save CSV As")
        if not path:
            return
        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["Product", "Quantity Sold"])
            for item, qty in sales.items():
                w.writerow([item, qty])
        messagebox.showinfo("Exported ✅", f"CSV saved to:\n{path}")

    # ── Register Customer tab ────────────────────────────────────────────────
    def _build_register_tab(self, parent):
        centre = card_frame(parent, padx=30, pady=24)
        centre.place(relx=0.5, rely=0.46, anchor="center", width=420)

        tk.Label(centre, text="👤 Register New Customer", font=FONT_HEAD,
                 bg=SURFACE, fg=GOLD).pack(pady=(0, 16))

        fields = [("Full Name", "reg_name"), ("Email", "reg_email"), ("Phone (11 digits)", "reg_phone")]
        for label, attr in fields:
            tk.Label(centre, text=label, font=FONT_BODY, bg=SURFACE, fg=TEXT).pack(anchor="w")
            var = tk.StringVar()
            setattr(self, attr, var)
            tk.Entry(centre, textvariable=var, font=FONT_BODY, width=30,
                     bg=BG, fg=TEXT, insertbackground=TEXT, relief="flat", bd=5).pack(pady=4, fill="x")

        styled_btn(centre, "✅ Register", self._register, color=GREEN, width=20).pack(pady=14)
        self.reg_msg = tk.Label(centre, text="", font=FONT_BODY, bg=SURFACE, fg=GREEN)
        self.reg_msg.pack()

    def _register(self):
        name  = self.reg_name.get().strip()
        email = self.reg_email.get().strip()
        phone = self.reg_phone.get().strip()
        if not name or not email or not phone:
            self.reg_msg.config(text="All fields are required.", fg=ACCENT)
            return
        if len(phone) != 11 or not phone.startswith(("010", "011", "012", "015")):
            self.reg_msg.config(text="Invalid phone number.", fg=ACCENT)
            return
        self.reg_msg.config(text=f"✅ {name} registered successfully!", fg=GREEN)


# ════════════════════════════════════════════════════════════════════════════
#  Run
# ════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    app = RestaurantApp()
    app.mainloop()
