def get_recommended_course(contract_id: Any, is_active: bool) -> dict | None:
    """
    Get recommended course
    :param contract_id: contract id in CRM
    :param is_active: asset status or no contract
    :return: dict recommended course or None

            Description:
            - Having a contract_id, we get the group number in the CRM
            - We get the course code from the contract number
            - If there are courses active > get data,
                                   none > None
            This exception causes a repeated search for
            the most similar course by title from the database and with
            a probability of 83% provides the correct recommendation
            This is due to the fact that the data in the
            CRM system is erroneous and they need to be,
            excluded in the future.
    """
    if not is_active:
        return None
    if not contract_id:
        return None
    number_class = 0
    code_course = None
    crm_code = None

    try:
        crm_contract_number = models.CRMContract.objects.get(id=contract_id)
        crm_code = models.CRMGroup.objects.get(id=crm_contract_number.group.id)
    except (MultipleObjectsReturned, ObjectDoesNotExist):
        return None
    code_course = edit_code_course(crm_code.group_name)
    number_class = crm_code.school

    try:
        course_in_recommendeddb = models.RecommendedCourse.objects.filter(
            class_level=number_class, code_courses=code_course
        )
        recommended_course = models.RecommendedCourse.objects.filter(
            num=course_in_recommendeddb[0].recommended_courses_num
        )
        course_direction = recommended_course[0].course_direction
        data = {
            "course_name": recommended_course[0].course_name,
            "course_direction": str(course_direction),
            "course_url": recommended_course[0].course_url,
            "course_start": recommended_course[0].course_start,
            "number_hours": recommended_course[0].number_hours,
            "price": price_month(recommended_course[0].price),
        }
        return data
    except (AttributeError, LookupError, ValueError):
        data = search_max_similarity(crm_code)
        return data


def price_month(price):
    """
    Get price in month
    :param price: price for the whole course 1944,0; 2131,0; 842,0;
    :return: price in month 239, 259, 99
    """
    price = price.replace(",", ".")
    price = round(float(price) / 8) - 10
    return f"{str(price)[:-1:]}9"