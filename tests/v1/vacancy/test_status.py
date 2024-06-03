import uuid


class TestStatus:
    async def test_vacancy_list_200(self, client, vacancy_status):
        response = await client.get("/api/v1/vacancy/")
        assert response.status_code == 200

    async def test_vacancy_200(self, client, vacancy_status):
        response = await client.get(f"/api/v1/vacancy/{str(vacancy_status.id)}/")
        assert response.status_code == 200

    async def test_vacancy_detail_404(self, client):
        response = await client.get(f"/api/v1/vacancy/{str(uuid.uuid4())}/")
        assert response.status_code == 404

    async def test_create_201(self, client, vacancy_status):
        data = {
            "city": {"name": "Nyandoma"},
            "company": {
                "name": "string",
                "description": "string",
            },
            "vacancy": {
                "title": "string",
                "description": "string",
                "language": "python",
                "speciality": "разработчик",
                "experience": "без опыта",
                "salary_from": 10000,
                "salary_to": 20000,
            },
            "tool": [{"name": "qwerty"}, {"name": "asdfg"}],
        }
        response = await client.post("/api/v1/vacancy/", json=data)
        assert response.status_code == 201

    async def test_create_422(self, client, vacancy_status):
        data = {
            "city": {"name": "Nyandoma"},
            # "company": {
            #     "name": "string",
            #     "description": "string",
            # },
            "vacancy": {
                "title": "string",
                "description": "string",
                "language": "python",
                "speciality": "разработчик",
                "experience": "без опыта",
                "salary_from": 10000,
                "salary_to": 20000,
            },
            "tool": [{"name": "qwerty"}, {"name": "asdfg"}],
        }
        response = await client.post("/api/v1/vacancy/", json=data)
        assert response.status_code == 422

    async def test_update_201(self, client, vacancy_status):
        data = {
            "city": {"name": "Nyandoma"},
            "company": {
                "name": "string",
                "description": "string",
            },
            "vacancy": {
                "title": "string2",
                "description": "string",
                "language": "python",
                "speciality": "разработчик",
                "experience": "без опыта",
                "salary_from": 100000,
                "salary_to": 200000,
            },
            "tool": [{"name": "asdfg"}],
        }
        response = await client.put(
            f"/api/v1/vacancy/{str(vacancy_status.id)}/", json=data
        )
        assert response.status_code == 201

    async def test_update_422(self, client, vacancy_status):
        data = {
            # "city": {
            #     "name": "Nyandoma"
            # },
            "company": {
                "name": "string",
                "description": "string",
            },
            "vacancy": {
                "title": "string2",
                "description": "string",
                "language": "python",
                "speciality": "разработчик",
                "experience": "без опыта",
                "salary_from": 100000,
                "salary_to": 200000,
            },
            "tool": [{"name": "asdfg"}],
        }
        response = await client.put(
            f"/api/v1/vacancy/{str(vacancy_status.id)}/", json=data
        )
        assert response.status_code == 422

    async def test_update_404(self, client, vacancy_status):
        data = {
            "city": {"name": "Nyandoma"},
            "company": {
                "name": "string",
                "description": "string",
            },
            "vacancy": {
                "title": "string2",
                "description": "string",
                "language": "python",
                "speciality": "разработчик",
                "experience": "без опыта",
                "salary_from": 100000,
                "salary_to": 200000,
            },
            "tool": [{"name": "asdfg"}],
        }
        response = await client.put(f"/api/v1/vacancy/{str(uuid.uuid4())}/", json=data)
        assert response.status_code == 404

    async def test_delete_204(self, client, vacancy_status):
        response = await client.delete(f"/api/v1/vacancy/{str(vacancy_status.id)}/")
        assert response.status_code == 204

    async def test_delete_404(self, client, vacancy_status):
        response = await client.delete(f"/api/v1/vacancy/{str(uuid.uuid4())}/")
        assert response.status_code == 404
