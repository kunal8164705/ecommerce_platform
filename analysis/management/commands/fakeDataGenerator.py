import pandas as pd
import numpy as np
from faker import Faker

# Initialize Faker to generate fake data
fake = Faker()

# Number of rows to generate
num_rows = 50000

# Generate the dataset
data = {
    'product_id': [_ for _ in range(num_rows)],
    'product_name': [fake.word().title() for _ in range(num_rows)],
    'category': [fake.random_element(elements=('Electronics', 'Clothing', 'Books', 'Home', 'Sports', 'Toys')) for _ in range(num_rows)],
    'price': [round(fake.random_number(digits=4), 2) for _ in range(num_rows)],
    'quantity_sold': [fake.random_int(min=1, max=1000) for _ in range(num_rows)],
    'rating': [round(fake.random.uniform(1.0, 5.0), 1) for _ in range(num_rows)],
    'review_count': [fake.random_int(min=0, max=500) for _ in range(num_rows)]
}

# Convert to a pandas DataFrame
df = pd.DataFrame(data)

# Save to a CSV file
df.to_csv('generated_products_dataset.csv', index=False)

print("Dataset generated and saved to 'generated_products_dataset.csv'")
