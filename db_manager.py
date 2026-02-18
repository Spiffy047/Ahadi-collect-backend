from app import app, db
from models import *
import click

@click.group()
def cli():
    """Database management commands"""
    pass

@cli.command()
def init():
    """Initialize database tables"""
    with app.app_context():
        db.create_all()
        click.echo("✅ Database tables created successfully!")

@cli.command()
def drop():
    """Drop all database tables"""
    with app.app_context():
        db.drop_all()
        click.echo("✅ All tables dropped successfully!")

@cli.command()
def reset():
    """Reset database (drop and recreate)"""
    with app.app_context():
        db.drop_all()
        db.create_all()
        click.echo("✅ Database reset successfully!")

@cli.command()
def seed():
    """Seed database with sample data"""
    from seed_database import seed_database
    seed_database()

@cli.command()
def status():
    """Show database status"""
    with app.app_context():
        try:
            # Test connection using ORM
            User.query.first()
            click.echo("✅ Database connection: OK")
            
            # Count records using ORM
            counts = {
                'Users': User.query.count(),
                'Regions': Region.query.count(),
                'Consumers': Consumer.query.count(),
                'Accounts': Account.query.count(),
                'Creditors': Creditor.query.count(),
                'Tags': Tag.query.count(),
                'Jobs': Job.query.count(),
                'Payments': Payment.query.count()
            }
            
            click.echo("\n📊 Record counts:")
            for table, count in counts.items():
                click.echo(f"  {table}: {count}")
                
        except Exception as e:
            click.echo(f"❌ Database error: {e}")

if __name__ == '__main__':
    cli()