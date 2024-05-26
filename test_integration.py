def test_converter_price_rec_courses() -> None:
    rate = price_month("1444,0")
    assert rate == "179"
    rate = price_month("1728,00")
    assert rate == "209"
    rate = price_month("960,00")
    assert rate == "119"


def test_recommended_course(
    authorized_client: Client,
    random_child_courses: alchemy.TestUserCourses,
) -> None:
    all_courses = authorized_client.get_courses_info()
    recommended_course = all_courses.children[0].courses[0].recommended_course
    assert recommended_course is not None
    assert (
        recommended_course.course_name
        == "Lego WeDo 2.0: Dino Park +EV3 (базовые модели)"
    )
    assert recommended_course.course_direction == "Робототехника"
    assert (
        recommended_course.course_url
        == "https://iteen.by/programs/4-class/robotiks-4-class/"
    )
    assert recommended_course.number_hours == "64"
    assert recommended_course.price == "109"


def test_max_similarity(
    psql_engine: sa.engine.Engine,
    mssql_engine: sa.engine.Engine,
    authorized_client: Client,
    random_child_courses: alchemy.TestUserCourses,
) -> None:
    all_courses = authorized_client.get_courses_info()
    contract_id = all_courses.children[0].courses[0].contract_id
    id_similarity = alchemy.get_max_similarity(
        psql_engine,
        mssql_engine,
        contract_id,
    )
    assert id_similarity == 17


def test_recommended_directions(
    authorized_client: Client,
    random_child_courses: alchemy.TestUserCourses,
) -> None:
    all_courses = authorized_client.get_courses_info()
    recommended_directions = all_courses.children[0].recommended_directions

    assert len(recommended_directions) == 7
    assert recommended_directions[0]["direction_name"] == "Все направления"
    assert recommended_directions[1]["direction_name"] == "Дизайн"
    assert recommended_directions[2]["direction_name"] == "Техномейкерство"
    assert (
        recommended_directions[3]["direction_name"]
        == "Программирование и Game Dev"
    )
    assert recommended_directions[4]["direction_name"] == "Авиамодели_БПЛА"
    assert recommended_directions[5]["direction_name"] == "Экспресс-курсы"
    assert (
        recommended_directions[6]["direction_name"]
        == "Спортивная робототехника"
    )


def test_bug_bciteen_1309(
    authorized_client: Client,
    random_child_courses: alchemy.TestUserCourses,
    random_user: alchemy.TestCrmUser,
    mssql_engine: sa.engine.Engine,
) -> None:
    all_courses = authorized_client.get_courses_info()
    assert all_courses.children != []
    alchemy.deactivate_contract(random_user, mssql_engine)

    all_courses = authorized_client.get_courses_info()
    assert all_courses.children != []
