from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal 

class ExpenseIncome(models.Model):
    """
    Represents an expense or income record.
    Each record is linked to a specific user.
    Includes fields for tax calculation based on flat or percentage rates.
    """
    TRANSACTION_TYPES = (
        ('credit', 'Credit (Income)'),
        ('debit', 'Debit (Expense)'),
    )

    TAX_TYPES = (
        ('flat', 'Flat Amount'),
        ('percentage', 'Percentage'),
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE, 
        related_name='expense_income_records', 
        help_text="The user who recorded this expense/income."
    )
    title = models.CharField(
        max_length=200,
        help_text="A brief title for the expense/income record."
    )
    description = models.TextField(
        blank=True,
        null=True,
        help_text="Optional detailed description for the record."
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="The base amount of the transaction before tax."
    )
    transaction_type = models.CharField(
        max_length=6, # 'credit' or 'debit'
        choices=TRANSACTION_TYPES,
        help_text="Type of transaction: 'credit' (income) or 'debit' (expense)."
    )
    tax = models.DecimalField( # This is the input tax value
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        help_text="The tax value. Interpreted as flat amount or percentage based on 'tax_type'."
    )
    tax_type = models.CharField(
        max_length=10, # 'flat' or 'percentage'
        choices=TAX_TYPES,
        default='flat',
        help_text="Type of tax calculation: 'flat' or 'percentage'."
    )
    date = models.DateField(
        help_text="The date when the record was made (YYYY-MM-DD)."
    )

    # Calculated fields, automatically set in the save method
    tax_amount_calculated = models.DecimalField( # Internal calculated tax amount
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        help_text="The calculated tax amount based on 'amount', 'tax', and 'tax_type'."
    )
    total_amount = models.DecimalField( # Internal total amount
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        help_text="The total amount including tax (amount + tax_amount_calculated)."
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when the record was created."
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Timestamp when the record was last updated."
    )

    class Meta:
        ordering = ['-date', '-created_at']

    def calculate_tax_and_total(self):
        """
        Calculates the tax_amount_calculated and total_amount based on
        the current amount, tax, and tax_type.
        """
        calculated_tax = Decimal('0.00')
        if self.tax_type == 'flat':
            calculated_tax = self.tax
        elif self.tax_type == 'percentage':
            calculated_tax = (self.amount * self.tax) / Decimal('100.00')

        self.tax_amount_calculated = calculated_tax.quantize(Decimal('0.01'))
        self.total_amount = (self.amount + self.tax_amount_calculated).quantize(Decimal('0.01'))

    def save(self, *args, **kwargs):
        """
        Overrides the save method to automatically calculate tax and total amount
        before saving the instance.
        """
        self.calculate_tax_and_total()
        super().save(*args, **kwargs)

    def __str__(self):
        """
        String representation of the ExpenseIncome object.
        """
        return f"{self.user.username} - {self.transaction_type.capitalize()}: {self.title} - {self.total_amount} on {self.date}"