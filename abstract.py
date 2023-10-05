from __future__ import annotations
from abc import ABC, abstractmethod
from random import randint

class AbstractFactory(ABC):
    """
    Soyut Fabrika arabirim, farklı soyut ürünleri döndüren bir dizi yöntemi tanımlar.
    Bu ürünler bir aileyi oluşturur ve genellikle bir aralarında işbirliği yapabilirler.
    Bir ürün ailesi birkaç farklı varyanta sahip olabilir, ancak bir varyantın ürünleri
    diğer varyantların ürünleriyle uyumsuz olabilir.
    """
    @abstractmethod
    def create_product_a(self) -> AbstractProductA:
        pass

    @abstractmethod
    def create_product_b(self) -> AbstractProductB:
        pass


class ConcreteFactory1(AbstractFactory):
    """
    Somut Fabrikalar, tek bir varyanta ait ürün ailesini üretir. Fabrika, sonuç ürünlerinin
    uyumlu olduğunu garanti eder. Unutmayın ki Somut Fabrika'nın yöntemlerinin imzaları
    soyut bir ürün döndürürken, yöntem içinde somut bir ürün örneği oluşturulur.
    """

    def create_product_a(self) -> AbstractProductA:
        return ConcreteProductA1()

    def create_product_b(self) -> AbstractProductB:
        return ConcreteProductB1()


class ConcreteFactory2(AbstractFactory):
    """
    Her Somut Fabrikanın karşılık gelen ürün varyantı vardır.
    """

    def create_product_a(self) -> AbstractProductA:
        return ConcreteProductA2()

    def create_product_b(self) -> AbstractProductB:
        return ConcreteProductB2()


class AbstractProductA(ABC):
    """
    Bir ürün ailesinin her farklı ürününün bir temel arabirimi olmalıdır. Tüm ürünlerin
    bu arabirimi uygulaması gerekmektedir.
    """

    @abstractmethod
    def useful_function_a(self) -> str:
        pass


"""
Somut Ürünler, karşılık gelen Somut Fabrikalar tarafından oluşturulur.
"""


class ConcreteProductA1(AbstractProductA):
    def useful_function_a(self) -> str:
        return randint(1, 100)


class ConcreteProductA2(AbstractProductA):
    def useful_function_a(self) -> str:
        return randint(101, 200)


class AbstractProductB(ABC):
    """
    İşte başka bir ürünün temel arabirimi. Tüm ürünler birbirleriyle etkileşim kurabilir,
    ancak doğru etkileşim yalnızca aynı somut varyantların ürünleri arasında mümkündür.
    """
    @abstractmethod
    def useful_function_b(self) -> None:
        """
        Product B is able to do its own thing...
        """
        pass

    @abstractmethod
    def another_useful_function_b(self, collaborator: AbstractProductA) -> None:
        """
        ...ancak aynı zamanda Ürün A ile işbirliği yapabilir.

        Soyut Fabrika, oluşturduğu tüm ürünlerin aynı varyanta ait olduğunu ve böylece uyumlu
        olduğunu garanti eder.
        """
        pass


"""
Somut Ürünler, karşılık gelen Somut Fabrikalar tarafından oluşturulur.
"""


class ConcreteProductB1(AbstractProductB):
    def useful_function_b(self) -> str:
        return "The result of the product B1."

    """
    Varyant, Ürün B1, yalnızca Varyant, Ürün A1 ile doğru şekilde çalışabilir. Bununla birlikte,
    AbstractProductA'nın herhangi bir örneğini kabul eder.
    """

    def another_useful_function_b(self, collaborator: AbstractProductA) -> str:
        result = collaborator.useful_function_a()
        return f"The result of the B1 collaborating with the ({result})"


class ConcreteProductB2(AbstractProductB):
    def useful_function_b(self) -> str:
        return "The result of the product B2."

    def another_useful_function_b(self, collaborator: AbstractProductA):
        """
        Varyant, Ürün B2, yalnızca Varyant, Ürün A2 ile doğru şekilde çalışabilir. Bununla birlikte,
        AbstractProductA'nın herhangi bir örneğini kabul eder.
        """
        result = collaborator.useful_function_a()
        return f"The result of the B2 collaborating with the ({result})"


def client_code(factory: AbstractFactory, num_operations: int) -> None:
    """
    İstemci kodu, fabrikaları ve ürünleri yalnızca soyut türlerle kullanır:
    AbstractFactory ve AbstractProduct. Bu, istemci koduna herhangi bir fabrika
    veya ürün alt sınıfını geçirmenize olanak tanır ve kodu bozmadan kullanabilirsiniz.
    """
    product_a = factory.create_product_a()
    results = [product_a.useful_function_a() for _ in range(num_operations)]
    print(f"Ürün: {product_a.__class__.__name__}")
    print(f"{num_operations} işlem sonucu: {results}")
    print(f"Toplam: {sum(results)}")


    product_b = factory.create_product_b()

    print(f"{product_b.useful_function_b()}")
    print(f"{product_b.another_useful_function_b(product_a)}", end="")


if __name__ == "__main__":
    """
    The client code can work with any concrete factory class.
    """
    num_operations = 5
    print("Client: Testing client code with the first factory type:")
    client_code(ConcreteFactory1(),num_operations)

    print("\n")

    print("Client: Testing the same client code with the second factory type:")
    client_code(ConcreteFactory2())