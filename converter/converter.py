import psycopg2
import matplotlib.pyplot as plt
from sqlalchemy.orm import Session
import shutil

from app.database.models.dnm import Dnm
from app.database.database import SessionLocal

import os
from dotenv import load_dotenv

load_dotenv()

db = SessionLocal()

DATABASE_URL = os.getenv("TRAFFICLIGHT_DATABASE_URL")

def fetch_data(query):
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data

def add_dnm_record(db: Session, dnmh_id: int, authored_id: str, url: str):
    new_record = Dnm(dnmh_id=dnmh_id, authored_id=authored_id, url=url)
    db.add(new_record)
    db.commit()
    db.refresh(new_record)
    return new_record.id

def create_and_save_graph(x_values, y_values, output_filename, color=True):
    fig, ax = plt.subplots(figsize=(8, 6), facecolor='white')

    if color:
        ax.plot(x_values, y_values, marker='o', linestyle='-', color='green', markersize=3, label='graph')
        ax.set_title('Динамограмма')
        ax.set_xlabel('Длина')
        ax.set_ylabel('Нагрузка')
    else:
        ax.plot(x_values, y_values, marker='o', linestyle='-', color='black', markersize=1)
        ax.set_facecolor('white')

        ax.set_title('')
        ax.set_xlabel('')
        ax.set_ylabel('')

    ax.set_xticks([])
    ax.set_yticks([])

    fig.savefig(output_filename, format='png', dpi=300, bbox_inches='tight', pad_inches=0.1)
    plt.close()

def get_random_unmarked_dinamogram(user_id: str):
    authored_unmarked_dnmh_data = db.query(Dnm).filter(
        (Dnm.authored_id == user_id) & (Dnm.marker_id == None)
    )

    if authored_unmarked_dnmh_data.count() > 0:
        output_filename = authored_unmarked_dnmh_data[0].url
        return output_filename

    else:
        dnmh_query = f'SELECT * FROM "Dnmh";'
        dnmh_data = fetch_data(dnmh_query)

        if dnmh_data:
            for dnmh_row in dnmh_data:
                dnmh_id = dnmh_row[0]
                count = db.query(Dnm).filter(
                    Dnm.dnmh_id == dnmh_id
                ).count()

                if not count > 0:
                    dnm_query = f'SELECT * FROM "Dnm" WHERE "Dnmh_Id" = {dnmh_id} ORDER BY "P";'
                    dnm_data = fetch_data(dnm_query)

                    x_values = [row[3] for row in dnm_data]
                    y_values = [row[4] for row in dnm_data]

                    filename = f'д_{dnmh_id}.png'

                    color_output_filename = f'datasets/raw/{filename}'
                    b_w_output_filename = f'datasets/clear/{filename}'

                    dnm_id = add_dnm_record(
                        db=db,
                        dnmh_id=dnmh_id,
                        authored_id=user_id,
                        url=filename
                    )

                    create_and_save_graph(x_values, y_values, color_output_filename, color=True)
                    create_and_save_graph(x_values, y_values, b_w_output_filename, color=False)

                    return {'id': dnm_id, "url": color_output_filename}
            return None

        else:
            return None

def mark_dinamogramm(id: int, marker_id: int):
    db.query(Dnm).filter(Dnm.id == id).update({"marker_id": marker_id})

    updated_dnm = db.query(Dnm).filter(Dnm.id == id).first()
    dnm_url = updated_dnm.url

    db.commit()

    output_filename = f'datasets/ready/д_{id}_{marker_id}.png'
    shutil.copy(f'datasets/clear/{dnm_url}', output_filename)

