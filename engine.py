from product import Product
from customer import Customer
from ordering import Ordering
from linkedlist import LinkedList, ProductLinkedList, CustomerLinkedList, OrderingLinkedList
from node import Node
from utils import formatted_input, clear
from copy import deepcopy

product_data, customer_data, ordering_data = ProductLinkedList(), CustomerLinkedList(), OrderingLinkedList()
product_table, customer_table = "",""
keep_track_quantity = 0


class Engine:
    def __init__(self):
        self.linkedlist = LinkedList()

    def display_data(self):
        return ""

    def save_object_list(self, file: str):
        with open(file, "w") as f:
            f.write(self.display_data())
            print("Save file successfully!!!")
        input("Press Enter to continue...")
        return f

    def search_by_object(self, code):
        node = self.linkedlist.search(code)
        if node:
            return node
        else:
            return "Not Found"

    def load_data_from_file(self, file):
        pass

    def option1(self, linkedlist):
        try:
            file = input("Enter the file name: ").strip()
            if file == "":
                return True
            else:
                self.linkedlist = linkedlist
                self.load_data_from_file(file)
        except:
            print("File format is invalid")
        input("Press Enter to continue...")

    def option3(self):
        print(self.display_data())
        input("Press Enter to continue...")

    def option4(self):
        file = input("Enter the file name (blank to quit): ").strip()
        if file == "":
            return True
        self.save_object_list(file)

    def option5(self):
        pcode = formatted_input("Enter pcode:")
        node = self.linkedlist.search(pcode)
        if node:
            print(node)
        else:
            print("Not Found")
        input("Press Enter to continue...")

    def option6(self):
        code = formatted_input("Delete code: ")
        try:
            if code == "":
                return True
            node = self.linkedlist.pop_code(code)
            assert node is not None
            if isinstance(node.data, Product):
                if not self.linkedlist.search(code):
                    print(f"Delete {node.data._pcode} successfully")
                else:
                    print(f"{code} does not exist!!!")

            if isinstance(node.data, Customer):
                if not self.linkedlist.search(code):
                    print(f"Delete {node.data._ccode} successfully")
                else:
                    print(f"{code} does not exist!!!")
        except Exception:
            print(f"{code} is invalid input")
        input("Press Enter to continue...")


class ProductEngine(Engine):
    def __init__(self):
        super().__init__()
        self.linkedlist = product_data

    def display_base_menu(self):
        return """
1.1.      Load data from file.
1.2.      Input & add to the end.
1.3.      Display data.
1.4.      Save product list to file.
1.5.      Search by pcode.
1.6.      Delete by pcode.
1.7.      Sort by pcode.
1.8.      Add after position k.
1.9.      Delete the node after the node having code = xCode.
1.0.      Quit.
        """

    def matching(self, stdin):
        match stdin:
            case "1":
                self.option1(ProductLinkedList())
                global product_data
                self.linkedlist = product_data
                return True
            case "2":
                while True:
                    try:
                        pcode = formatted_input("Enter pcode (blank to leave): ")
                        if pcode == "":
                            return True
                        elif (
                            pcode[0] != "P"
                            or (pcode[0] == "P" and not pcode[1:].isdigit())
                            or len(pcode) < 3
                        ):
                            print(
                                "Invalid product code. The format should be: P<number>. E.g: P02, P299..."
                            )
                            continue
                        elif self.search_by_object(pcode) != "Not Found":
                            print(f"The pcode: {pcode} already exist.")
                            continue
                        pro_name = formatted_input("Enter pro_name: ").capitalize()
                        if pro_name == "":
                            continue
                        quantity = int(formatted_input("Enter quantity: "))
                        saled = int(formatted_input("Enter saled (saled <= quantity): "))
                        if saled > quantity:
                            print("Invalid input!!!")
                            continue
                        price = float(formatted_input("Enter price: "))
                        product = Product(pcode, pro_name, quantity, saled, price)
                        self.linkedlist.append(Node(product))
                        input("Press Enter to continue...")
                        return True
                    except:
                        print("Invalid input!!!")
                        continue
            case "3":
                self.option3()
                return True
            case "4":
                self.option4()
                return True
            case "5":
                self.option5()
                return True
            case "6":
                self.option6()
                return True
            case "7":
                temp = deepcopy(self.linkedlist)
                self.linkedlist.sort_by_object()
                self.option3()
                self.linkedlist = temp
                return True
            case "8":
                while True:
                    try:
                        pcode = formatted_input("Enter pcode (blank to leave): ")
                        if pcode == "":
                            return self.linkedlist
                        elif (
                            pcode[0] != "P"
                            or (pcode[0] == "P" and not pcode[1:].isdigit())
                            or len(pcode) < 3
                        ):
                            print(
                                "Invalid product code. The format should be: P<number>. E.g: P02, P299..."
                            )
                            continue
                        elif self.search_by_object(pcode) != "Not Found":
                            print(f"The pcode: {pcode} already exist.")
                            continue
                        pro_name = formatted_input("Enter pro_name: ").capitalize()
                        if pro_name == "":
                            continue
                        quantity = int(formatted_input("Enter quantity: "))
                        saled = int(formatted_input("Enter saled (saled <= quantity): "))
                        if saled > quantity:
                            print("Invalid input!!!")
                            continue
                        price = float(formatted_input("Enter price: "))
                        product = Product(pcode, pro_name, quantity, saled, price)
                        index = int(formatted_input("Insert index (start from 0):"))
                        if index == "":
                            return True
                        elif index < 0 or index > len(self.linkedlist):
                            return True
                        self.linkedlist.insert_after_index(index, Node(product))
                        print(f"Insert after index {index} successfully")
                        input("Press Enter to continue...")
                        return True
                    except:
                        print("Invalid input!!!")
                        continue
            case "9":
                pcode = formatted_input("Enter pcode: ")
                self.delete_after_pcode(pcode)
                input("Press Enter to continue...")
                return True
            case "0":
                product_data = self.linkedlist
                return False
            case _:
                return True

    def load_data_from_file(self, file: str, delimiter: str = "|"):
        try:
            with open(file, "r") as f:
                for i in map(
                    lambda lst: map(lambda char: char.strip(), lst),
                    map(
                        lambda line: line.split(delimiter),
                        filter(None, f.read().splitlines()),
                    ),
                ):
                    pcode, pro_name, quantity, saled, price = i
                    pcode, pro_name, quantity, saled, price = (
                        pcode,
                        pro_name,
                        int(quantity),
                        int(saled),
                        float(price),
                    )
                    node = Node(Product(pcode, pro_name, quantity, saled, price))
                    self.linkedlist.append(node)
                    global product_data
                    product_data = self.linkedlist
            print("Loading file successfully!!!")
            return product_data

        except FileNotFoundError:
            print(f'File: "{file}" not found')
            return product_data

    def display_data(self):
        space = 15
        first_line = f"{'ProductCode':<{space}}|{'Pro_name':<{space}}|{'Quantity':<{space}}|{'Saled':<{space}}|{'Price':<{space}}|{'Value':<{space}}"
        separate_line = "-" * space * 6
        detail = ""
        for node in self.linkedlist:
            data = node.data
            pcode = data._pcode
            pro_name = data._pro_name
            quantity = data._quantity
            saled = data._saled
            price = data._price
            value = f"{data._saled * data._price:.1f}"
            detail += f"{pcode:<{space}}|{pro_name:<{space}}|{quantity:<{space}}|{saled:<{space}}|{price:<{space}}|{value:<{space}}\n"
        table = f"{first_line}\n{separate_line}\n{detail}"
        global product_table
        product_table = table
        return table

    def delete_after_pcode(self, pcode: str):
        if pcode == "":
            return True
        node = self.linkedlist.pop_after_code(pcode)

        if node:
            print(f"Delete after {node._pcode} successfully")
        elif not self.linkedlist.search(pcode):
            print(f"{pcode} does not exist!!!")
        else:
            print(f"No pcode after {pcode}")


class CustomerEngine(Engine):
    def __init__(self):
        super().__init__()
        self.linkedlist = customer_data

    def load_data_from_file(self, file: str, delimiter: str = "|"):
        try:
            with open(file, "r") as f:
                for i in map(
                    lambda lst: map(lambda char: char.strip(), lst),
                    map(lambda line: line.split(delimiter), f.readlines()),
                ):
                    ccode, name, phone = i
                    node = Node(Customer(ccode, name, phone))
                    self.linkedlist.append(node)
                    global customer_data
                    customer_data = self.linkedlist
            print("Loading file successfully!!!")
            return customer_data

        except FileNotFoundError:
            print(f'File: "{file}" not found')
            return customer_data

    def matching(self, stdin):
        match stdin:
            case "1":
                self.option1(CustomerLinkedList())
                global customer_data
                self.linkedlist = customer_data
                return True
            case "2":
                while True:
                    try:
                        ccode = formatted_input("Enter ccode (blank to leave): ")
                        if ccode == "":
                            return True
                        elif (
                            ccode[0] != "C"
                            or (ccode[0] == "C" and not ccode[1:].isdigit())
                            or len(ccode) < 3
                        ):
                            print(
                                "Invalid product code. The format should be: C<number>. E.g: C02, C299..."
                            )
                            continue
                        elif self.search_by_object(ccode) != "Not Found":
                            print(f"The pcode: {ccode} already exist.")
                            continue
                        name = formatted_input("Enter name: ").capitalize()
                        phone = int(formatted_input("Enter phone: "))
                        customer = Customer(ccode, name, str(phone))
                        self.linkedlist.append(Node(customer))
                        input("Press Enter to continue...")
                        return True
                    except:
                        print("Invalid input!!!")
                        continue
            case "3":
                self.option3()
                return True
            case "4":
                self.option4()
                return True
            case "5":
                self.option5()
                return True
            case "6":
                self.option6()
                return True
            case "0":
                customer_data = self.linkedlist
                return False
            case _:
                return True

    def display_base_menu(self):
        return """
2.1.      Load data from file
2.2.      Input & add to the end
2.3.      Display data
2.4.      Save customer list to file
2.5.      Search by ccode
2.6.      Delete by ccode
2.0.      Quit
        """

    def display_data(self):
        space = 15
        first_line = f"{'CustomerCode':<{space}}|{'Name':<{space}}|{'Phone':<{space}}"
        separate_line = "-" * space * 3
        detail = ""
        for node in self.linkedlist:
            data = node.data
            ccode = data._ccode
            name = data._cus_name
            phone = data._phone
            detail += f"{ccode:<{space}}|{name:<{space}}|{phone:<{space}}\n"
        table = f"{first_line}\n{separate_line}\n{detail}"
        global customer_table
        customer_table = table
        return table


class OrderingEngine(Engine):
    def __init__(self):
        super().__init__()
        self.linkedlist = ordering_data

    def matching(self, stdin):
        match stdin:
            case "1":
                while True:
                    try:
                        pcode = formatted_input("Enter pcode (blank to leave): ")
                        product_search = product_data.search(pcode)
                        if pcode == "":
                            #  return self.linkedlist
                            return True
                        elif (
                            pcode[0] != "P"
                            or (pcode[0] == "P" and not pcode[1:].isdigit())
                            or len(pcode) < 3
                        ):
                            print(
                                "Invalid product code. The format should be: P<number>. E.g: P02, P299..."
                            )
                            continue
                        elif product_search == False:
                            print(f"{pcode} is not in database")
                            continue
                        ccode = formatted_input("Enter ccode: ")
                        global customer_data
                        customer_search = customer_data.search(ccode)
                        if (
                            ccode[0] != "C"
                            or (ccode[0] == "C" and not ccode[1:].isdigit())
                            or len(ccode) < 3
                        ):
                            print(
                                "Invalid product code. The format should be: C<number>. E.g: C02, C299..."
                            )
                            continue
                        elif customer_search == False:
                            print(f"{ccode} is not in database")
                            continue
                        global ordering_data
                        if ordering_data.search_pcode(pcode) and ordering_data.search_ccode(ccode):
                            print(f"{pcode} and {ccode} already in order list!!!")
                            continue

                        if product_search and customer_search:
                            assert isinstance(product_search, Product)
                            if product_search._saled == product_search._quantity:
                                print("The product is exhauted")
                                continue
                            else:
                                print(f"{pcode} has {product_search._quantity - product_search._saled} remainders")

                        quantity = int(input(("Enter quantity: ")))
                        assert isinstance(product_search, Product)
                        if quantity <= (product_search._quantity - product_search._saled):
                            self.linkedlist.append(Node(Ordering(pcode, ccode, quantity)))
                            product_search._saled += quantity
                            print("Order successfully!!!")
                            global keep_track_quantity
                            keep_track_quantity = quantity
                        else:
                            print("Not enough item to order!!!")
                            continue
                        input("Press Enter to continue...")
                        return True
                    except:
                        print("Invalid input!!!")
                        continue
            case "2":
                self.option3()
                return True
            case "3":
                temp = deepcopy(self.linkedlist)
                self.linkedlist.sort_by_object()
                self.option3()
                self.linkedlist = temp
                return True
            case "0":
                ordering_data = self.linkedlist
                return False
            case _:
                return True

    def display_base_menu(self):
        return """
3.1.      Input data
3.2.      Display data with total value
3.3.      Sort by pcode + ccode
3.0.      Quit
"""
    def display_data(self):
        space = 15
        first_line = f"{'Pcode':<{space}}|{'Ccode':<{space}}|{'Value':<{space}}"
        separate_line = "-" * space * 3
        detail = ""
        for node in self.linkedlist:
            data = node.data
            pcode = data._pcode
            ccode = data._ccode
            value = f"{keep_track_quantity * product_data.search(pcode)._price:.1f}"
            detail += f"{pcode:<{space}}|{ccode:<{space}}|{value:<{space}}\n"
        table = f"{first_line}\n{separate_line}\n{detail}"
        return table


if __name__ == "__main__":
    customer_engine = CustomerEngine()
    customer_engine.load_data_from_file("customer.txt")
    customer_engine.option3()
    product_engine = ProductEngine()
    product_engine.load_data_from_file("product.txt")
    product_engine.linkedlist.append(Node(Product("P08", "Banh Mi", 12, 12, 0.1)))
    product_engine.option3()
    ordering = OrderingEngine()
    while True:
        ordering.matching("1")
        ordering.matching("2")
        ordering.matching("3")
