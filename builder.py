from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any

class Builder(ABC):
    """
    Builder arayüzü, Ürün nesnelerinin farklı parçalarını oluşturmak için yöntemleri belirtir.
    """

    @property
    @abstractmethod
    def product(self) -> None:
        pass

    @abstractmethod
    def produce_part_a(self) -> None:
        pass

    @abstractmethod
    def produce_part_b(self) -> None:
        pass

    @abstractmethod
    def produce_part_c(self) -> None:
        pass

class ConcreteBuilder1(Builder):
    """
    Somut Builder sınıfları Builder arayüzünü takip eder ve inşa adımlarının özel uygulamalarını sağlar.
    Programınız farklı Builder varyasyonlarına sahip olabilir ve bunlar farklı şekillerde uygulanabilir.
    """

    def __init__(self) -> None:
        """
        Yeni bir builder örneği, daha sonra montajda kullanılan boş bir ürün nesnesi içermelidir.
        """
        self.reset()

    def reset(self) -> None:
        self._product = Product1()

    @property
    def product(self) -> Product1:
        """
        Somut Builder'lar sonuçları almak için kendi yöntemlerini sağlamalıdır.
        Çünkü farklı türdeki builder'lar tamamen farklı ürünler oluşturabilir ve aynı arayüzü izlemeyebilir.
        Bu nedenle, bu tür yöntemler, temel Builder arayüzünde (en azından tip güvenli bir programlama dilinde) 
        bildirilemez.

        Genellikle sonucu istemciye döndürdükten sonra, bir builder örneğinin başka bir ürün oluşturmaya başlamak 
        üzere hazır olması beklenir. Bu nedenle, genellikle getProduct yöntemi sonunda reset yöntemini çağırmak alışılmış bir 
        uygulamadır. Ancak bu davranış zorunlu değildir ve builder'larınızın önceki sonuçları atmadan istemci kodundan 
        açık bir reset çağrısı beklemesini sağlayabilirsiniz.
        """
        product = self._product
        self.reset()
        return product

    def produce_part_a(self) -> None:
        self._product.add("ParçaA1")

    def produce_part_b(self) -> None:
        self._product.add("ParçaB1")

    def produce_part_c(self) -> None:
        self._product.add("ParçaC1")

class Product1():
    """
    Builder desenini yalnızca ürünleriniz oldukça karmaşıksa ve geniş bir yapılandırmaya ihtiyaç duyuyorsa 
    kullanmak mantıklıdır. Diğer oluşturucu desenlerinin aksine, farklı somut builder'lar ilgisiz ürünler oluşturabilir. 
    Yani çeşitli builder'ların sonuçları her zaman aynı arayüzü izlemeyebilir.
    """

    def __init__(self) -> None:
        self.parts = []

    def add(self, part: Any) -> None:
        self.parts.append(part)

    def list_parts(self) -> None:
        print(f"Ürün parçaları: {', '.join(self.parts)}", end="")

class Director:
    """
    Director, inşa adımlarını belirli bir sırayla yürüten tek sorumludur. Ürünleri belirli bir sıraya veya yapılandırmaya göre oluşturmak istendiğinde veya yapılandırmak istendiğinde yararlıdır. Katı bir şekilde düşünüldüğünde, Director sınıfı isteğe bağlıdır, çünkü istemci builder'ları doğrudan kontrol edebilir.
    """

    def __init__(self) -> None:
        self._builder = None

    @property
    def builder(self) -> Builder:
        return self._builder

    @builder.setter
    def builder(self, builder: Builder) -> None:
        """
        Director, istemci kodu tarafından iletilen herhangi bir builder örneğiyle çalışır. Bu şekilde istemci kodu yeni monte edilen ürünün nihai türünü değiştirebilir.
        """
        self._builder = builder

    """
    Director, aynı inşa adımlarını kullanarak birkaç ürün çeşidini oluşturabilir.
    """

    def build_minimal_viable_product(self) -> None:
        self.builder.produce_part_a()

    def build_full_featured_product(self) -> None:
        self.builder.produce_part_a()
        self.builder.produce_part_b()
        self.builder.produce_part_c()

if __name__ == "__main__":
    """
    İstemci kodu bir builder nesnesi oluşturur, bunu direktöre ileterek ve ardından inşa sürecini başlatarak çalışır. Sonuç builder nesnesinden alınır.
    """

    director = Director()
    builder = ConcreteBuilder1()
    director.builder = builder

    print("Standart temel ürün: ")
    director.build_minimal_viable_product()
    builder.product.list_parts()

    print("\n")

    print("Standart tam özellikli ürün: ")
    director.build_full_featured_product()
    builder.product.list_parts()

    print("\n")

    # Unutmayın, Builder deseni bir Director sınıfı olmadan da kullanılabilir.
    print("Özel ürün: ")
    builder.produce_part_a()
    builder.produce_part_b()
    builder.product.list_parts()
