from __future__ import annotations
from abc import ABC, abstractmethod

class Creator(ABC):
    """
    Creator sınıfı, bir Product sınıfının bir nesnesini döndürmesi gereken bir factory method'u tanımlar.
    Creator'ın alt sınıfları genellikle bu yöntemin uygulanmasını sağlar.
    """

    @abstractmethod
    def factory_method(self):
        """
        Creator ayrıca factory method'un bazı varsayılan uygulamalarını sağlayabilir.
        """
        pass

    def some_operation(self, num1, num2) -> str:
        """
        Ayrıca, Creator'ın başlıca sorumluluğunun ürünler oluşturmak olmadığını unutmayın.
        Genellikle, Product nesneleri tarafından döndürülen işletme mantığına dayanan bazı temel iş mantığı içerir.
        Alt sınıflar, factory method'u geçersiz kılabilir ve bu yöntemi kullanarak farklı bir ürün türünü döndürebilir.
        """

        # Factory method'u çağırarak bir Product nesnesi oluştu.
        product = self.factory_method()

        result = product.operation(num1, num2)

        return result

class ConcreteCreator1(Creator):
    """
    Not olarak, yöntemin imzası hala soyut bir ürün türü kullanır, 
    ancak aslında yöntemden döndürülen somut ürünün türüdür. 
    Bu şekilde Creator, somut ürün sınıflarından bağımsız kalabilir.
    """

    def factory_method(self):
   
        return ConcreteProduct1()

class ConcreteCreator2(Creator):
    def factory_method(self):
        return ConcreteProduct2()

class Product(ABC):
    """
    Product arayüzü, tüm somut ürünlerin uygulaması gereken işlemleri tanımlar.
    """

    @abstractmethod
    def operation(self) -> str:

        return "{Product classınındaki operation foksiyonu çalıştı}"

"Concrete Creators, sonuç ürünün türünü değiştirmek için factory method'unu geçersiz kılarlar."

class ConcreteProduct1(Product):
    def operation(self, product_1, product_2) -> str:
        x = product_1 + product_2
        return x
        # return "{ConcreteProduct1'in Sonucu}"

class ConcreteProduct2(Product):
    def operation(self) -> str:
        return "{ConcreteProduct2'nin Sonucu}"

def client_code(creator: Creator, number1, number2) -> None:
    """
    İstemci kodu, bir somut yaratıcı örneğiyle çalışır, ancak hala temel arayüzü üzerinden.
    İstemci, yaratıcıyı temel arayüzü üzerinden çalıştırdığı sürece, herhangi bir yaratıcı alt sınıfını iletebilir.
    """

    print(f"İstemci: Yaratıcının sınıfını bilmiyorum, ama yine de çalışıyor.\n")
    return creator.some_operation(number1, number2)

if __name__ == "__main__":
 
    a = client_code(ConcreteCreator1(), 10, 5)
    print("\n")

    print("Uygulama: ConcreteCreator2 ile başlatıldı.")
    client_code(ConcreteCreator2())
