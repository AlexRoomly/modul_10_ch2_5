from multiprocessing import Process, Manager

class WarehouseManager:
    def __init__(self):
        self.data = Manager().dict()
        # Атрибут data - словарь, где ключ - название продукта, а значение
        # - его кол-во. (изначально пустой)

    def run(self, requests):
        # Метод run - принимает запросы и создаёт для каждого свой параллельный процесс,
        # запускает его(start) и замораживает(join)
        process = []
        for request in requests:
            proc = Process(target=self.process_request, args=(request,))
            proc.start()
            proc.join()

    def process_request(self, request):
        name, action, quantity = request
        if action == 'receipt':
            if name in self.data:
                self.data[name] += quantity
            else:
                self.data[name] = quantity
        if action == 'shipment':
            if name in self.data and self.data[name] > 0:
                self.data[name] -= quantity


if __name__ == '__main__':
    # Создаем менеджера склада
    manager = WarehouseManager()

    # Множество запросов на изменение данных о складских запасах
    requests = [
        ("product1", "receipt", 100),
        ("product2", "receipt", 150),
        ("product1", "shipment", 30),
        ("product3", "receipt", 200),
        ("product2", "shipment", 50)
    ]

    # Запускаем обработку запросов
    manager.run(requests)

    # Выводим обновленные данные о складских запасах
    print(manager.data)
    # вывод консоли: {"product1": 70, "product2": 100, "product3": 200}
