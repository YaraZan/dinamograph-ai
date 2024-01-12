import psycopg2
import matplotlib.pyplot as plt

# Подключение к бд
db_params = {
    'host': '10.1.27.137',
    'database': 'pgLightDB',
    'user': 'postgres',
    'password': '1qA2wS3eD',
}

# Функция для парсинга данных с бд
def fetch_data(query):
    conn = psycopg2.connect(**db_params)
    cursor = conn.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data

# Функция создания графика и сохранения как изображения
def create_and_save_graph(x_values, y_values, output_filename):
    plt.plot(x_values, y_values, marker='o', linestyle='-', label='graph')
    plt.title('Динамограмма')
    plt.xlabel('Длина')
    plt.ylabel('Нагрузка')
    plt.legend()
    plt.savefig(output_filename, format='png', dpi=300, bbox_inches='tight')
    plt.close()

# Парсинг данных с бд
well_query = f'SELECT * FROM "Well"'
well_data = fetch_data(well_query)

# Итерация через каждую запись в таблице "Well"
for well_row in well_data:
    well_id = well_row[0]

    # Выбор подходящей записи из таблицы "Dnmh"
    dnmh_query = f'SELECT * FROM "Dnmh" WHERE "Well_Id" = {well_id};'
    dnmh_data = fetch_data(dnmh_query)

    if dnmh_data:
        dnmh_row = dnmh_data[0]
        dnmh_id = dnmh_row[0]

        # Выбрать все записи соответствующие "Dnmh_Id"
        dnm_query = f'SELECT * FROM "Dnm" WHERE "Dnmh_Id" = {dnmh_id} ORDER BY "P";'
        dnm_data = fetch_data(dnm_query)

        # Выборка значений x и y из данных
        x_values = [row[3] for row in dnm_data]
        y_values = [row[4] for row in dnm_data]

        # Создание и сохранение графика
        output_filename = f'output/динамограмма_{well_id}.png'
        create_and_save_graph(x_values, y_values, output_filename)
        print(f'График для скважины {well_id} сохранён как {output_filename}')
    else:
        print(f'Нет динамограммы для скважины {well_id}')

print('Конвертация завершена.')