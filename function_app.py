import azure.functions as func
import logging
import uuid
from azure.functions.decorators.core import DataType

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.function_name(name="HttpCombined")
@app.route(route="HttpExample")
@app.queue_output(arg_name="msg", queue_name="outqueue", connection="AzureWebJobsStorage")
@app.generic_output_binding(
    arg_name="toDoItems",
    type="sql",
    CommandText="dbo.ToDo",
    ConnectionStringSetting="SqlConnectionString",
    data_type=DataType.STRING)
def HttpCombined(req: func.HttpRequest, 
                 msg: func.Out[func.QueueMessage], 
                 toDoItems: func.Out[func.SqlRow]) -> func.HttpResponse:
    
    logging.info('HTTP trigger function: simultaneously writing to Queue and SQL.')
    name = req.params.get("name") or req.get_json().get("name", "Anonymous")
    
    # set Queue message
    msg.set(name)

    # set SQL row
    row = func.SqlRow({
        "Id": str(uuid.uuid4()),
        "title": name,
        "completed": False,
        "url": ""
    })
    toDoItems.set(row)

    return func.HttpResponse(f"Hello {name}, your data has been sent to both Queue and SQL.")