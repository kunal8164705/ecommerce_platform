import pandas as pd
from analysis.models import Product
from functools import reduce
from django.db import transaction, DatabaseError
from django.db import transaction
class UploadCleanDataSet:

    def __init__(self) -> None:
        # Initialize the class by getting all fields of the Product model.
        try:
            self.columns = set(["product_name","category","price","quantity_sold","rating","review_count"])
        except AttributeError as e:
            raise Exception("Error retrieving model fields: " + str(e))

    @staticmethod
    def CleanDataSetAsPerGivenRules(df: pd.DataFrame) -> pd.DataFrame:
        try:
           # Fill missing 'price' values with the median price.
            df['price'] = df['price'].fillna(df['price'].median())
            # Fill missing 'quantity_sold' values with the median quantity.
            df['quantity_sold'] = df['quantity_sold'].fillna(df['quantity_sold'].median())
            # Fill missing 'rating' values with the mean rating within each category.
            df['rating'] = df.groupby('category')['rating'].transform(lambda x: x.fillna(x.mean()))
        except KeyError as e:
            raise Exception("Error cleaning dataset: Missing expected column " + str(e))
        except Exception as e:
            raise Exception("Unexpected error during dataset cleaning: " + str(e))
        return df
    
    @staticmethod
    def ConvertToKeyValueHasMap(df: pd.DataFrame) -> dict:
        try:
            # Convert DataFrame into a dictionary where keys are product IDs and values are product details.
            return reduce(
                lambda acc, product: {**acc, product["product_id"]: product},
                df.to_dict(orient="records"),  # Ensure each row is converted into a dictionary.
                {}
            )
        except KeyError as e:
            raise Exception("Error converting DataFrame to dictionary: Missing expected column " + str(e))
        except Exception as e:
            raise Exception("Unexpected error during dictionary conversion: " + str(e))
    
    @transaction.atomic
    def processDataSetToDatabase(self, path):
        try:
            # Read the CSV file and clean the dataset as per the rules.
            df_dict = self.ConvertToKeyValueHasMap(df=self.CleanDataSetAsPerGivenRules(df=pd.read_csv(path)))

            UpdatedSet = set()  # Track IDs of products that need updating.
            products = Product.objects.filter(id__in=list(df_dict.keys()))

            for product in products:
                UpdatedSet.add(product.id)
                UpdateDetails = df_dict[product.id]
                UpdateAbleFields = self.columns.intersection(set(UpdateDetails.keys()))

                # Update only the fields that exist in both the Product model and the CSV.
                for column in UpdateAbleFields:
                    try:
                        setattr(product, column, UpdateDetails[column])
                    except Exception as e:
                        raise Exception(f"Error updating product {product.id}: " + str(e))
            
            BULK_ADD = []  
            # Prepare a list for bulk creation of new products.
            for newProduct in df_dict.keys() - UpdatedSet:
                prod = df_dict[newProduct]
                prod.pop("product_id")
                BULK_ADD.append(Product(**df_dict[newProduct]))

            with transaction.atomic():
                # Perform bulk update for existing products.
                if products:
                    try:
                        Product.objects.bulk_update(products, fields=self.columns, batch_size=20)
                    except DatabaseError as e:
                        raise Exception("Error during bulk update: " + str(e))
                # Perform bulk create for new products.
                if BULK_ADD:
                    try:
                        Product.objects.bulk_create(BULK_ADD, batch_size=30)
                    except DatabaseError as e:
                        raise Exception("Error during bulk create: " + str(e))
        
        except pd.errors.EmptyDataError:
            raise Exception("CSV file is empty. Please provide a valid file.")
        except FileNotFoundError as e:
            raise Exception("CSV file not found: " + str(e))
        except Exception as e:
            raise Exception("Unexpected error during data processing: " + str(e))
