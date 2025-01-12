from fasthtml.common import *
import matplotlib.pyplot as plt

# Import QueryBase, Employee, Team from employee_events
#### YOUR CODE HERE
from employee_events import QueryBase, Employee, Team

# import the load_model function from the utils.py file
#### YOUR CODE HERE
from .utils import load_model

"""
Below, we import the parent classes
you will use for subclassing
"""
from base_components import Dropdown, BaseComponent, Radio, MatplotlibViz, DataTable

from combined_components import FormGroup, CombinedComponent


# Create a subclass of base_components/dropdown
# called `ReportDropdown`
class ReportDropdown(Dropdown):
    #### YOUR CODE HERE

    # Overwrite the build_component method
    # ensuring it has the same parameters
    # as the Report parent class's method
    #### YOUR CODE HERE
    #  Set the `label` attribute so it is set
    #  to the `name` attribute for the model
    #### YOUR CODE HERE

    # Return the output from the
    # parent class's build_component method
    #### YOUR CODE HERE
    def build_component(self, model, asset_id):
        self.label = model.name
        return super().build_component(model, asset_id)

    # Overwrite the `component_data` method
    # Ensure the method uses the same parameters
    # as the parent class method
    #### YOUR CODE HERE
    # Using the model argument
    # call the employee_events method
    # that returns the user-type's
    # names and ids
    def component_data(self, model, asset_id):
        return model.user_data(asset_id)


# Create a subclass of base_components/BaseComponent
# called `Header`
class Header(BaseComponent):
    pass
    #### YOUR CODE HERE

    # Overwrite the `build_component` method
    # Ensure the method has the same parameters
    # as the parent class
    #### YOUR CODE HERE

    # Using the model argument for this method
    # return a fasthtml H1 objects
    # containing the model's name attribute
    #### YOUR CODE HERE
    def build_component(self, model, *args, **kwargs):
        return H1(model.name)


# Create a subclass of base_components/MatplotlibViz
# called `LineChart`
class LineChart(MatplotlibViz):

    def visualization(self, entity_id, model):
        df = model.event_counts(entity_id)
        df = df.fillna(0)
        df = df.set_index("date")
        df = df.sort_index()
        df = df.cumsum()
        df.columns = ["Positive", "Negative"]
        fig, ax = plt.subplots()
        df.plot(ax=ax)
        self.set_axis_styling(ax)
        ax.set_title("Cumulative Event Counts")
        ax.set_xlabel("Date")
        ax.set_ylabel("Event Count")
        return fig


# Create a subclass of base_components/MatplotlibViz
# called `BarChart`
#### YOUR CODE HERE
class BarChart(MatplotlibViz):
    pass
    # Create a `predictor` class attribute
    # assign the attribute to the output
    # of the `load_model` utils function
    #### YOUR CODE HERE
    predictor = load_model()

    # Overwrite the parent class `visualization` method
    # Use the same parameters as the parent
    #### YOUR CODE HERE
    def visualization(self, entity_id, model):

        # Using the model and asset_id arguments
        # pass the `asset_id` to the `.model_data` method
        # to receive the data that can be passed to the machine
        # learning model
        #### YOUR CODE HERE

        # Using the predictor class attribute
        # pass the data to the `predict_proba` method
        #### YOUR CODE HERE

        # Index the second column of predict_proba output
        # The shape should be (<number of records>, 1)
        #### YOUR CODE HERE

        # Below, create a `pred` variable set to
        # the number we want to visualize
        #
        # If the model's name attribute is "team"
        # We want to visualize the mean of the predict_proba output
        #### YOUR CODE HERE

        # Otherwise set `pred` to the first value
        # of the predict_proba output
        #### YOUR CODE HERE

        # Initialize a matplotlib subplot
        #### YOUR CODE HERE

        # Run the following code unchanged
        ax.barh([""], [pred])
        ax.set_xlim(0, 1)
        ax.set_title("Predicted Recruitment Risk", fontsize=20)

        # pass the axis variable
        # to the `.set_axis_styling`
        # method
        #### YOUR CODE HERE


# Create a subclass of combined_components/CombinedComponent
# called Visualizations
#### YOUR CODE HERE
class Visualizations(CombinedComponent):
    # Set the `children`
    # class attribute to a list
    # containing an initialized
    # instance of `LineChart` and `BarChart`
    #### YOUR CODE HERE

    # Leave this line unchanged
    outer_div_type = Div(cls="grid")


# Create a subclass of base_components/DataTable
# called `NotesTable`
class NotesTable(DataTable):
    pass


#### YOUR CODE HERE

# Overwrite the `component_data` method
# using the same parameters as the parent class
#### YOUR CODE HERE

# Using the model and entity_id arguments
# pass the entity_id to the model's .notes
# method. Return the output
#### YOUR CODE HERE


class DashboardFilters(FormGroup):

    id = "top-filters"
    action = "/update_data"
    method = "POST"

    children = [
        Radio(
            values=["Employee", "Team"],
            name="profile_type",
            hx_get="/update_dropdown",
            hx_target="#selector",
        ),
        ReportDropdown(id="selector", name="user-selection"),
    ]


# Create a subclass of CombinedComponents
# called `Report`
#### YOUR CODE HERE
class Report(CombinedComponent):
    # Set the `children`
    # class attribute to a list
    # containing initialized instances
    # of the header, dashboard filters,
    # data visualizations, and notes table
    #### YOUR CODE HERE
    children = [NotesTable(), Visualizations(), Header(), DashboardFilters()]


# Initialize a fasthtml app
#### YOUR CODE HERE
app = FastHTML()
# Initialize the `Report` class
#### YOUR CODE HERE
report = Report()

# Create a route for a get request
# Set the route's path to the root
#### YOUR CODE HERE


# Call the initialized report
# pass None and an instance
# of the QueryBase class as arguments
# Return the result
#### YOUR CODE HERE
@app.get("/")
def home_page():
    return report(None, QueryBase())


# Create a route for a get request
# Set the route's path to receive a request
# for an employee ID so `/employee/2`
# will return the page for the employee with
# an ID of `2`.
# parameterize the employee ID
# to a string datatype
#### YOUR CODE HERE


# Call the initialized report
# pass the ID and an instance
# of the Employee SQL class as arguments
# Return the result
#### YOUR CODE HERE
@app.get("/employee/{employee_id}")
def employee_endpoint(employee_id: str):
    return report(employee_id, Employee())


# Create a route for a get request
# Set the route's path to receive a request
# for a team ID so `/team/2`
# will return the page for the team with
# an ID of `2`.
# parameterize the team ID
# to a string datatype
#### YOUR CODE HERE


# Call the initialized report
# pass the id and an instance
# of the Team SQL class as arguments
# Return the result
#### YOUR CODE HERE
@app.get("/team/{team_id}")
def team_endpoint(team_id: str):
    return report(team_id, Team())


# Keep the below code unchanged!
@app.get("/update_dropdown{r}")
def update_dropdown(r):
    dropdown = DashboardFilters.children[1]
    print("PARAM", r.query_params["profile_type"])
    if r.query_params["profile_type"] == "Team":
        return dropdown(None, Team())
    elif r.query_params["profile_type"] == "Employee":
        return dropdown(None, Employee())


@app.post("/update_data")
async def update_data(r):
    from fasthtml.common import RedirectResponse

    data = await r.form()
    profile_type = data._dict["profile_type"]
    id = data._dict["user-selection"]
    if profile_type == "Employee":
        return RedirectResponse(f"/employee/{id}", status_code=303)
    elif profile_type == "Team":
        return RedirectResponse(f"/team/{id}", status_code=303)


serve()
