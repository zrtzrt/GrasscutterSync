# GrasscutterSync
Synchronize your account to Grasscutter

---
### Running
1. setup [Grasscutter](https://github.com/Grasscutters/Grasscutter) to build database
   1. `account <username> [UID]`
   2. login account and choose your main character
   3. backup your database before running script
2. run [Inventory_Kamera](https://github.com/Andrewthe13th/Inventory_Kamera) to get json data from your account
4. run main.py and input `UID`, `JSON DATA PATH` 
    ```
    pip install pymongo
    python main.py
    ```

---
### Bonus
 - put data/Banners.json to Grasscutter/data