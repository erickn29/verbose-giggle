from v1.vacancy.model.model import Language, Speciality, Experience


class Analyzer:
    SPECIALITIES = {
        Speciality.devops.value: (
            "devops",
            "девопс"
        ),
        Speciality.machine_learning.value: (
            "nlp",
            "llm",
            "ds",
            "deep learning",
            "машинное",
            "machine learning",
            "машинного",
            "нейронщик",
        ),
        Speciality.analyst.value: (
            "аналитик",
            "analyst",
            "бизнес-аналитик",
            "бизнес аналитик",
            "продуктовый аналитик",
            'руководитель отдела аналитики',
            "системный аналитик",
            "system analyst",
            "bi",
        ),
        Speciality.data_science.value: (
            "дата-сайентист",
            "дата сайентист",
            "data engineer",
            "analyst",
            "базами данных",
            "базы данных",
            "баз данных",
            "data",
            "data science",
        ),
        Speciality.project_manager.value: (
            "менеджер продукта",
            "менеджер проектов"
        ),
        Speciality.developer.value: (
            "web-разработчик",
            "программист",
            "разработчик",
            "веб-разработчик",
            "developer",
            "frontend-разработчик",
            "инженер-программист",
            "backend-разработчик",
            "бекенд-программист",
            "backend",
            "frontend",
            "web-программист",
            "fullstack-разработчик",
            "фронтенд-разработчик",
            "мидл-разработчик",
            "backend-developer",
            "программист-разработчик",
            "инженер-разработчик",
            "ml-разработчик",
            "инженер",
            "software engineer",
        ),
        Speciality.team_lead.value: (
            "руководитель группы разработки",
            "lead",
            "руководитель группы",
            "тимлид",
            "teamlead",
            "руководитель команды разработки",
            "TeamLead",
        ),
        Speciality.system_administrator.value: (
            "системный администратор",
            "linux-администратор",
            "системный инженер",
        ),
        Speciality.cyber_security.value: (
            "специалист по информационной безопасности",
            "pentest",
        ),
        Speciality.qa.value: (
            "тестировщик",
            "qa",
            "qa-специалист",
            "автотестировщик",
            "тестированию",
        ),
    }

    LANGUAGES_MAPPING = {
        ("Python", "python"): Language.python.value,
        ("PHP",): Language.php.value,
        ("C++", "С++", "СС++", "C", "С/С++"): Language.plus_plus.value,
        ("C#", "С#"): Language.sharp.value,
        (
            "JavaScript",
            "JS",
            "react.js",
            "Frontend",
            "Node.JS",
            "React.js",
            "React",
            "Node.js",
            "Vue",
            "Angular",
            "Frontend-разработчик",
        ): Language.javascript.value,
        ("Java", "JAVA", "Spring"): Language.java.value,
        ("Golang", "GO", "Go"): Language.golang.value,
        ("Rust",): Language.rust.value,
    }

    HH_EXPERIENCE = {
        "noExperience": Experience.no_experience.value,
        "between1And3": Experience.one_to_three.value,
        "between3And6": Experience.three_to_five.value,
        "moreThan6": Experience.more_than_five.value,
    }

    def __init__(
        self,
        title: str = None,
        description: str = None,
        tools: list = None,
        experience: str = None,
    ):
        self.title = title
        self.description = description
        self.tools = tools
        self.experience = experience

    @staticmethod
    def _clean_text(text: str) -> str:
        clean_text = (
            text
            .replace("&lt;", "")
            .replace("&gt;", "")
            .replace("/li", "")
            .replace("/ul", "")
            .replace("<p>", "")
            .replace("</p>", "")
            .replace("<em>", "")
            .replace("</em>", "")
            .replace("<b>", "")
            .replace("</b>", "")
            .replace("<i>", "")
            .replace("</i>", "")
            .replace("<strong>", "")
            .replace("</strong>", "")
            .replace("<li>", "")
            .replace("</li>", "")
            .replace("<ul>", "")
            .replace("</ul>", "")
            .replace("<>", "")
            .replace(",", "")
        )
        return clean_text

    def _match_language(self, text: str) -> str | None:
        cleaned_list = self._clean_text(text).split(" ")
        for word in cleaned_list:
            for lang_tuple, lang_name in Analyzer.LANGUAGES_MAPPING.items():
                if word in lang_tuple:
                    return lang_name

    def _match_speciality(self, text: str) -> str | None:
        for word in self._clean_text(text).split(" "):
            for speciality_name, speciality_tuple in Analyzer.SPECIALITIES.items():
                if word.lower() in speciality_tuple:
                    return speciality_name

    def get_language(self):
        if self.title:
            if language := self._match_language(self.title):
                return language
        if self.description:
            if language := self._match_language(self.description):
                return language
        if self.tools:
            if language := self._match_language(" ".join(self.tools)):
                return language

    def get_speciality(self):
        if self.title:
            if speciality := self._match_speciality(self.title):
                return speciality
        if self.description:
            if speciality := self._match_speciality(self.description):
                return speciality
        if self.tools:
            if speciality := self._match_speciality(" ".join(self.tools)):
                return speciality

    def get_head_hunter_experience(self):
        if self.experience:
            return self.HH_EXPERIENCE.get(self.experience)
