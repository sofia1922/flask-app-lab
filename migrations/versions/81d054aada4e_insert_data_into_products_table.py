from alembic import op
import sqlalchemy as sa

revision = '81d054aada4e'
down_revision = '6138cfe7a737'
branch_labels = None
depends_on = None

def upgrade():
    op.execute("""
        INSERT OR IGNORE INTO categories (name) VALUES
        ('Smartphones'),
        ('Laptops'),
        ('Accessories');
    """)

    op.execute("""
        INSERT INTO products (name, price, active, created_at, category_id) VALUES
        ('iPhone 15', 999.99, 1, CURRENT_TIMESTAMP, 1),
        ('Gaming Laptop', 1500.00, 1, CURRENT_TIMESTAMP, 2),
        ('Wireless Headphones', 199.00, 1, CURRENT_TIMESTAMP, 3);
    """)


def downgrade():
    # відкат — видалення вставлених записів
    op.execute("""
        DELETE FROM products WHERE name IN (
            'iPhone 15', 'Gaming Laptop', 'Wireless Headphones'
        );
    """)
    op.execute("""
        DELETE FROM categories WHERE name IN (
            'Smartphones', 'Laptops', 'Accessories'
        );
    """)
