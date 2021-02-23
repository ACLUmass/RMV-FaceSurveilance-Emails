library(shiny)
library(shinycssloaders)
library(profvis)

# Define UI for application that draws a histogram
shinyUI(fluidPage(

    # Application title
    titlePanel("Facial Recognition: Emails"),
    textInput("From", "From:", placeholder="Karen"),
    actionButton("apply_filters_button", "Apply Filters"),

    textOutput("n_emails"),
    
    withSpinner(uiOutput("emails"), type=4, color="#b5b5b5", size=0.5)
))
