"""
Протестируйте классы из модуля homework/models.py
"""
import pytest

from models import Product, Cart


@pytest.fixture
def product():
    return Product(name="book", price=100, description="This is a book", quantity=1000)


@pytest.fixture
def cart():
    return Cart()


class TestProducts:
    """
    Тестовый класс - это способ группировки ваших тестов по какой-то тематике
    Например, текущий класс группирует тесты на класс Product
    """

    @pytest.mark.parametrize("el", [0, 1, 999, 1000])
    def test_product_check_quantity_valid_qty(self, product, el):
        # TODO напишите проверки на метод check_quantity

        assert product.check_quantity(el) is True

    @pytest.mark.parametrize("el", [1001, -1])
    def test_product_check_quantity_invalid_qty(self, product, el):
        assert product.check_quantity(el) is False

    def test_product_buy(self, product):
        # TODO напишите проверки на метод buy

        product.buy(0)
        assert product.quantity == 1000

        product.buy(1)
        assert product.quantity == 999

        product.buy(999)
        assert product.quantity == 0

    def test_product_buy_more_than_available(self, product):
        # TODO напишите проверки на метод buy,
        #  которые ожидают ошибку ValueError при попытке купить больше, чем есть в наличии

        with pytest.raises(ValueError) as exception:
            product.buy(1001)
        assert str(exception.value) == 'Запрашиваемое количество недоступно'


class TestCart:
    """
    TODO Напишите тесты на методы класса Cart
        На каждый метод у вас должен получиться отдельный тест
        На некоторые методы у вас может быть несколько тестов.
        Например, негативные тесты, ожидающие ошибку (используйте pytest.raises, чтобы проверить это)
    """

    def test_add_one_product_to_cart(self, product, cart):
        cart.add_product(product)

        assert len(cart.products) == 1
        assert cart.products[product] == 1

    def test_add_the_same_product_twice_to_cart(self, product, cart):
        cart.add_product(product)
        cart.add_product(product)

        assert len(cart.products) == 1
        assert cart.products[product] == 2

    def test_add_10_quantity_of_product_to_cart(self, product, cart):
        cart.add_product(product, 10)

        assert len(cart.products) == 1
        assert cart.products[product] == 10

    def test_add_quantity_more_than_available_to_cart(self, product, cart):
        with pytest.raises(ValueError) as exception:
            cart.add_product(product, 1001)
        assert str(exception.value) == 'Недоступно требуемое количество'

    def test_add_quantity_more_than_available_on_second_attempt(self, product, cart):
        with pytest.raises(ValueError) as exception:
            cart.add_product(product, 900)
            cart.add_product(product, 101)
        assert str(exception.value) == 'Недоступно требуемое количество'

    def test_remove_product_with_no_remove_quantity_from_cart(self, product, cart):
        cart.add_product(product, 10)
        cart.remove_product(product)

        assert len(cart.products) == 0

    def test_remove_product_with_quantity_greater_than_quantity_in_the_cart(self, product, cart):
        cart.add_product(product, 10)
        cart.remove_product(product, 100)

        assert len(cart.products) == 0

    def test_remove_product_with_partial_quantity_from_cart(self, product, cart):
        cart.add_product(product, 10)
        cart.remove_product(product, 3)

        assert len(cart.products) == 1
        assert cart.products[product] == 7

    def test_remove_product_with_full_quantity_from_cart(self, product, cart):
        cart.add_product(product, 10)
        cart.remove_product(product, 10)

        assert len(cart.products) == 0

    def test_clear_cart(self, product, cart):
        cart.add_product(product, 10)
        cart.clear()

        assert len(cart.products) == 0

    def test_get_total_price_of_products_in_cart(self, product, cart):
        cart.add_product(product, 10)

        assert cart.get_total_price() == 1000

    def test_buy_products_with_valid_quantity_from_cart(self, product, cart):
        cart.add_product(product, 10)
        cart.buy()

        assert len(cart.products) == 0
        assert product.quantity == 990
