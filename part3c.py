#- *- coding: utf- 8 - *-
import sqlite3
import datetime

db= sqlite3.connect('/Users/kat/OneDrive - Solent University/database assignment/part_1.db')
cursor= db.cursor()


def manage_product (choice_cat):
    sql_query = "select p.category_id,p.product_id, p.product_description, p.product_status\
                from products p\
                where category_id = ? AND product_status IS \'Available'\
                order by p.category_id"
    cursor.execute(sql_query, (choice_cat,))
    all_choice_cat_rows = cursor.fetchall()
    if all_choice_cat_rows:
        print("Category ID\tProduct ID\tProduct Description\t\t\t     Product Status\n")
        for choice_cat_row in all_choice_cat_rows:
            category_id = choice_cat_row[0]
            product_id = choice_cat_row[1]
            product_description = choice_cat_row[2]
            product_status = choice_cat_row[3]
            print("{0:8}\t{1:10}\t{2:45}{3:20}"\
            .format(category_id,product_id,product_description, product_status))
        choice_buy =int(input("\nEnter the ID of the product you would like to purchase:\n"))
        #selecting a product to buy
        sql_query = "SELECT ps.seller_id, s.seller_name, ps.price\
                    FROM product_sellers ps\
                        inner join sellers s ON ps.seller_id= s.seller_id\
                    where ps.product_id = ?\
                    order by s.seller_name"
        cursor.execute(sql_query, (choice_buy,))
        all_choice_buy_rows = cursor.fetchall()
        if all_choice_buy_rows:
            print("\nSeller ID\tSeller Name\t    Price\n")
            for choice_buy_row in all_choice_buy_rows:
                seller_id = choice_buy_row[0]
                seller_name = choice_buy_row[1]
                price = choice_buy_row[2]
                print("{0:8}\t{1:15}\t{2:10.2f}"\
                .format(seller_id,seller_name,price))
            #selecting a seller to buy from
            choice_seller =int(input("\nEnter the ID of the seller you would like to purchase from:\n"))
            sql_query = "select ps.price, ps.seller_id, ps.product_id\
                            from product_sellers ps\
                            where ps.seller_id =? and ps.product_id=?"
            cursor.execute(sql_query, (choice_seller, choice_buy))
            choice_price_row = cursor.fetchone()
            choice_price = choice_price_row[0]
            choice_qty =int(input("\nEnter the quantity you would like to purchase:\n"))
            print("Product " +str(choice_buy) + " from the seller " + str(choice_seller) +" at a price " +str(choice_price)+". Quantity: " + str(choice_qty))
            add_to_basket = int(input("\nAdd to basket? Press 1. for Yes, 2. for No.\n"))
            if add_to_basket == 1:
                try:
                    
                    cursor.execute("PRAGMA foreign_keys=ON")
                    cursor.execute("select basket_id\
                    from shopper_baskets\
                    where shopper_id= ?",(shopper_id,))
        
                    active_basket= cursor.fetchone()
                    
                    
                    if active_basket:
                        active_basket_id= active_basket[0]
                        #if the user has an active basket, use it to add new products
                        sql_insert = "INSERT INTO basket_contents(basket_id, product_id, seller_id, quantity, price)\
                                    VALUES(?,?,?,?,?)"
                        cursor.execute(sql_insert,(active_basket_id, choice_buy, choice_seller, choice_qty, choice_price))
                        print("\nAdded to basket.\n")
                        db.commit()
                        print("\nGoing back to the main menu...\n")
                    else:
                    #create a new basket ID
                        cursor.execute("select seq + 1 \
                            from sqlite_sequence \
                            WHERE name = 'shopper_baskets'")
                        seg_row = cursor.fetchone()
                        next_basket_id = seg_row[0]
                        now=datetime.datetime.now()
                        todays_date = now.strftime("%d-%m-%Y")
                        sql_insert = "INSERT INTO shopper_baskets(basket_id,shopper_id, basket_created_date_time)\
                                    VALUES (?,?,?)"
                        cursor.execute(sql_insert,(next_basket_id,shopper_id, todays_date))
                        print("\nAdded to basket.\n")
                        db.commit()
                        print("\nGoing back to the main menu...\n")
                    run== False
                except db.Error:
                    print("\nSomething went wrong, rolling back changes...\n")
                    db.rollback()
            elif add_to_basket == 2:
                print("\nYou didn't add to the basket. Loading main menu...\n\n")
                run == False
            else:
                    print("\nInvlid entry. Loading main menu....\n\n")
                    run == False

        else:
            print("\nNo sellers sell this product. Loading main menu... \n\n")
            run == False
    else:
        print("\nNo products available. Loading main menu... \n\n")
        run == False


run= True
customer = True 

print("\n\n  _____   ______ _____ __   _  _____  _______  _____")
print(" |     | |_____/   |   | \  | |     | |       |     |")
print(" |_____| |    \_ __|__ |  \_| |_____| |_____  |_____|")
print("_____________________________________________________")
print("\n\nWelcome to ORINOCO\n\n")

#selecting a shopper ID
while customer:
    shopper_id = input("\nPlease enter your shopper ID number: \n")
    sql_query= "SELECT shopper_id\
                FROM shoppers\
                WHERE shopper_id=?"
    cursor.execute(sql_query, (shopper_id,))
    shopper_id_row = cursor.fetchone()
    if shopper_id_row:
        shopper_id_id = shopper_id_row[0]
        print("\nCustomer {0} has logged on\n\n".format(shopper_id))
        break
    else:
        customer == False
        print("\nNo customer found with that id.")

    
while run:
    #displaying a main menu    
    print ('ORINOCO - SHOPPER MAIN MENU')
    print('_______________________________')
    print('\n 1. Display your order history')
    print('\n 2. Add an item to your basket')
    print('\n 3. View your basket')
    print('\n 4. Checkout')
    print('\n 5. Exit \n')
    choice = int(input('Choose one of the options: \n'))

    #selecing 1.
    if choice == 1:
        sql_query= "SELECT so.order_id as 'order ID', so.order_date as 'order date', p.product_description as 'product description', ss.seller_name as 'seller name' , op.price AS 'price', op.quantity as 'qty', op.ordered_product_status as 'status' \
            FROM shoppers s \
            LEFT OUTER JOIN shopper_orders so ON s.shopper_id = so.shopper_id \
            LEFT OUTER JOIN ordered_products op ON so.order_id = op.order_id \
            LEFT OUTER JOIN products p ON op.product_id = p.product_id \
            left outer join sellers ss on op.seller_id = ss.seller_id \
            WHERE s.shopper_id= ?  \
            ORDER BY so.order_date DESC"
        cursor.execute(sql_query, (shopper_id,))
        all_choice_rows = cursor.fetchall()
        if all_choice_rows:
            print("Orders of the customer {0}:".format(shopper_id))
            print("Order ID\tOrder date\tProduct Description \t\t\t\t\t\t\tSeller\t\t   Price\tQty\tStatus\n")
            for choice_row in all_choice_rows:
                order_id = choice_row[0]
                order_date = choice_row[1]
                product_description = choice_row[2]
                seller_name = choice_row[3]
                price = choice_row[4]
                quantity = choice_row[5]
                ordered_product_status = choice_row[6]
                print("{0:8}\t{1:10}\t{2:70}\t{3:10}\t{4:9.2f}\t{5:3}\t{6:20}"\
                    .format(order_id, order_date, product_description, seller_name, price, quantity, ordered_product_status))
            if_continue= input("Press 1 to go back to the main menu\n")
            if if_continue == 1:
                run== False
        else:
            print("\nNo orders yet.\n")
    #selecting 2.        
    elif choice == 2:
        print("\nCategories:\n")
        print("1.Mobile phones and accessories")
        print("2.TV and Home Cinema")
        print("3.Cameras and accessories")
        print("4.Audio and Hifi")
        print("5.Computers and accessories")
        print("6.Gaming\n")
        choice_cat = int(input("Choose a category:\n"))
        #selecting  a category
        if choice_cat == 1:
            print("\nCATEGORY: Mobile phones and accessories:\n")
            manage_product(choice_cat)
    
        elif choice_cat == 2:
            print("\nCATEGORY: TV and Home Cinema:\n")
            manage_product(choice_cat)
            
        elif choice_cat == 3:
            print("\nCATEGORY: Cameras and accessories:\n")
            manage_product(choice_cat)

        elif choice_cat == 4:
            print("\nCATEGORY: Audio and Hifi:\n")
            manage_product(choice_cat)
            
        elif choice_cat == 5:
            print("\nCATEGORY: Computers and accessories:\n")
            manage_product(choice_cat)

        elif choice_cat == 6:
            print("\nCATEGORY: Gaming:\n")
            manage_product(choice_cat)

    #selecting 3.
    elif choice == 3:
        print("Basket Contents:")
        print("___________________\n")
        #looking if there is an active basket for that user
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.execute("select basket_id\
                    from shopper_baskets\
                    where shopper_id= ?",(shopper_id,))
        active_basket= cursor.fetchone()
                    

        if active_basket:
            active_basket_id= active_basket[0]
            sql_query= "select p.product_description, s.seller_name, bc.quantity, bc.price\
                    from basket_contents bc\
                    left outer join product_sellers ps on bc.seller_id = ps.seller_id\
                    left outer join products p on  ps.product_id= p.product_id\
                    left outer join sellers s on ps.seller_id=s.seller_id\
                    where basket_id = ?\
                    group by product_description" 
            cursor.execute(sql_query, (active_basket_id,))
            all_basket_rows = cursor.fetchall()
            if all_basket_rows:
                print("Product Description\t\t\t\t\t\t\tSeller Name\t\tQty\t    Price\n")
                for basket_row in all_basket_rows:
                    product_description = basket_row[0]
                    seller_name = basket_row[1]
                    quantity = basket_row[2]
                    price = basket_row[3]
                    print("{0:70}\t{1:20}\t{2:4}\t{3:10}"\
                        .format(product_description, seller_name, quantity, price))
                if_continue= input("\nPress 1 to go back to the main menu:\n")
                if if_continue == 1:
                    run== False
        else:
            print("No orders yet.")
            print("Going back to the main menu...\n")


    #selecting 4.
    elif choice == 4:
        print("Not done yet")

    #selecting 5
    elif choice == 5:
        exit= int(input("\nAre you sure you want to exit? \nclick 1. for yes 2. for no /n\n"))
        if exit == 1:
            run = False
       
    else:
            print("\n\nInvalid entry. displaying menu...\n")
            print("\nPlease select one of the following options:\n")
           
#quit connection with the database
db.close()
