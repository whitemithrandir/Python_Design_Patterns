from abc import ABC, abstractmethod

# Ürün Arabirimi
class Movie(ABC):
    @abstractmethod
    def list_details(self) -> None:
        pass

# Film sınıfı (Somut Ürün)
class LordOfTheRingsMovie(Movie):
    def __init__(self):
        self.details = {}

    def list_details(self) -> None:
        print("Film Detayları:")
        for key, value in self.details.items():
            print(f"{key}: {value}")

# Builder Arabirimi
class MovieBuilder(ABC):
    @property
    @abstractmethod
    def movie(self) -> Movie:
        pass

    @abstractmethod
    def set_director(self, director: str) -> None:
        pass

    @abstractmethod
    def add_actor(self, actor: str) -> None:
        pass

    @abstractmethod
    def set_location(self, location: str) -> None:
        pass

# Film Üretimi (ConcreteBuilder)
class LordOfTheRingsMovieBuilder(MovieBuilder):
    def __init__(self):
        self.reset()

    def reset(self) -> None:
        self._movie = LordOfTheRingsMovie()

    @property
    def movie(self) -> Movie:
        movie = self._movie
        self.reset()
        return movie

    def set_director(self, director: str) -> None:
        self._movie.details["Yönetmen"] = director

    def add_actor(self, actor: str) -> None:
        if "Oyuncular" not in self._movie.details:
            self._movie.details["Oyuncular"] = []
        self._movie.details["Oyuncular"].append(actor)

    def set_location(self, location: str) -> None:
        self._movie.details["Geçtiği Ortam"] = location

# Director
class MovieDirector:
    def __init__(self):
        self._builder = None

    @property
    def builder(self) -> MovieBuilder:
        return self._builder

    @builder.setter
    def builder(self, builder: MovieBuilder) -> None:
        self._builder = builder

    def build_movie(self) -> None:
        self.builder.set_director("Peter Jackson")
        self.builder.add_actor("Sauron")
        self.builder.add_actor("Gandalf")
        self.builder.set_location("Mordor")

if __name__ == "__main__":
    director = MovieDirector()
    movie_builder = LordOfTheRingsMovieBuilder()
    director.builder = movie_builder

    print("\n")
    
    print("Yüzüklerin Efendisi filmi oluşturuluyor:")
    director.build_movie()
    movie_builder.movie.list_details()
