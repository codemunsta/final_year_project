import PyPDF2


def school_fees_check(doc_name, mat_no, session):
    school_fees = open(doc_name, 'rb')
    pdf_reader = PyPDF2.PdfFileReader(school_fees)
    page_obj = pdf_reader.getPage(0)
    text = page_obj.extractText()
    array = text.splitlines()
    line_number = 0

    if array[line_number] == 'University of Benin':
        for line in text.splitlines():
            line_number = line_number + 1
            if line == 'Matriculation Number:':
                varry = array[line_number]
                if varry == mat_no:
                    print('you have a mat number')
                else:
                    message = 'matriculation number does not match'
                    return message
            if line == 'Payment Category:':
                varry = array[line_number]
                if varry == 'School Fee':
                    print('this is a schoolfees printout')
                else:
                    message = 'wrong document provided'
                    return message
            if line == 'Payment Session:':
                varry = array[line_number]
                if varry == session:
                    print('this is the correct seasion')
                else:
                    message = 'this payment is not for current academic session'
                    return message
            if line == 'Payment State:':
                varry = array[line_number]
                if varry == 'Paid':
                    print('you have paid school fees')
                else:
                    message = 'you have not paid'
                    return message
            if line == 'Response Description:':
                varry = array[line_number]
                if varry == 'Approved':
                    print('payment has been approved')
                    return 0
                else:
                    message = 'payment not yet approved'
                    return message
        message = 'incorrect document'
        print(message)
        return message
    else:
        message = 'wrong document provided'
        return message


def bed_allocation_check(doc_name, mat_no, session):
    bed_allocation = open(doc_name, 'rb')
    pdf_reader = PyPDF2.PdfFileReader(bed_allocation)
    page_obj = pdf_reader.getPage(0)
    text = page_obj.extractText()
    array = text.splitlines()
    line_number = 0

    if array[line_number] == 'University of Benin':
        for line in text.splitlines():
            line_number = line_number + 1
            if line == 'Matriculation Number:':
                varry = array[line_number]
                if varry == mat_no:
                    print('you have a mat number')
                else:
                    message = 'matriculation number does not match'
                    return message
            if line == 'Payment Category:':
                varry = array[line_number]
                if varry == 'Bed Allocation Fee':
                    print('this is a bed allocation printout')
                else:
                    message = 'wrong document provided'
                    return message
            if line == 'Payment Session:':
                varry = array[line_number]
                if varry == session:
                    print('this is the correct session')
                else:
                    message = 'this payment is not for current academic session'
                    return message
            if line == 'Payment State:':
                varry = array[line_number]
                if varry == 'Paid':
                    print('you have paid for bed allocation')
                else:
                    message = 'you have not paid'
                    return message
            if line == 'Activation Code:':
                activation_code = array[line_number]
                print(activation_code)
            if line == 'Response Description:':
                varry = array[line_number]
                if varry == 'Approved':
                    print('payment has been approved')
                    return 0
                else:
                    message = 'payment not yet approved'
                    return message
    else:
        message = 'wrong document provided'
        return message
    message = 'wrong document provided'
    return message
