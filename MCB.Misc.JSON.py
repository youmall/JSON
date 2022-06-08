from typing import Any

def MapTo_PropertyValue (Value :object) -> str:
# Returns 'ERROR' on error, else a String representing a JSON Property Value
    
    if Value == None: return 'null' # Note: This is a String value
    
    v_ValueType = type(Value)
    if v_ValueType is int or v_ValueType is float:
        v_Property_Value = str(Value)
    elif v_ValueType is str:
        if Value == 'ERROR': return 'ERROR' # i.e. Error
        if Value.startswith('{'):    # i.e. Indicates Value is a JSON Object representation
            v_Property_Value = Value    # Do not enclose the JSON Object value between double quotes
        else:
            v_Property_Value = '"' + Value + '"'  # Enclose the value between double quotes
        #end if
    elif v_ValueType is list:
        if len(Value) == 0:
            v_Property_Value = '[]'
        else:
            v_Property_Value = '['
            for item in Value:
                item_Property_Value = MapTo_PropertyValue (item)  # Recursion
                if item_Property_Value == 'ERROR': return 'ERROR' # i.e. Error
                v_Property_Value = v_Property_Value + item_Property_Value + ','
            #end For
            v_Property_Value = v_Property_Value[0:-1] + ']' # Remove last ',' and append ']'
        #end if
    else:   # Not a valid v_ValueType
        return 'ERROR' # i.e. Error
    #end if
    return v_Property_Value
# end def


def Add ( Name :str, Value :object, JSON_Str :str = None) -> Any:
# Returns None on error, else a String representing a JSON Object

    if Name == None: return None # i.e. Error
    if not(type(Name) is str): return None # i.e. Error
    v_Name = Name.strip()
    if v_Name == '': return None # i.e. Error

    if JSON_Str == None:
        v_Str = '{}'
    else:
        if not(type(JSON_Str) is str): return None # i.e. Error
        v_Str = JSON_Str.strip()
        if v_Str == '':
            v_Str = '{}'
        elif len(v_Str) < 2 or v_Str[0] != '{' or v_Str[-1] != '}':
            return None # i.e. Error
        #end if    
    #end if
        
    v_Property_Value = MapTo_PropertyValue (Value)
    if v_Property_Value == 'ERROR': return None #i.e. Error

    v_Str = v_Str[0:-1]   # Get all of v_Str except last '}' character
    if v_Str != '{': v_Str = v_Str + ','   # Add ',' because Property to be added is not the 1st one
    
    return ( v_Str + '"' + v_Name + '": ' + v_Property_Value + '}')
 # end def


bank = 'MCB'
employees = [ 
    {   "firstName": "Emp 1 FN",
        "middlename": None,
        "lastName": "Emp 1 LN",
        "yearJoinedBank": 2000,
        "locations": ["St Jean", "WFH", 418.4, None],
        "addresses": []
    },
    {   "firstName": "Emp 2 FN",
        "middlename": None,
        "lastName": "",
        "yearJoinedBank": 2005,
        "locations": ["", "WFH", -418.4, None],
        "addresses": []
    },
]


log = []
errorOccurred = False

try:
    employees_JSON_List = []
    for employee in employees:
        emp_JSON_str = ""
        for key in employee:
            log.append(f"Processing Employee Key \"{key}\" = {employee[key]}")
            emp_JSON_str = Add(key, employee[key], emp_JSON_str)
            log.append(f"emp_JSON_str: {emp_JSON_str}")
            if emp_JSON_str == None: raise Exception()
        # Finished processing all keys in an employee
        log.append (f"Employee's emp_JSON_str: {emp_JSON_str}")
        employees_JSON_List.append(emp_JSON_str)
    # Finished processing all employees
    log.append (f"All employees: {str(employees_JSON_List)}")
    mcb_JSON_str = Add("bank", bank)
    mcb_JSON_str = Add("employees", employees_JSON_List, mcb_JSON_str)
    log.append (f"mcb_JSON_str: {mcb_JSON_str}")

except:
    errorOccurred = True

finally:
    
    if errorOccurred:
        print ("ERROR OCCURRED")
        for item in log:
            print(f"\n{item}\n")
    else:
        print (mcb_JSON_str)
