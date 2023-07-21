from jazzmin.dashboard import AbstractDashboard

class CustomDashboard(AbstractDashboard):
    def init_with_context(self, context):
        self.children.append({
            "title": "Welcome",
            "description": "Customize your dashboard here!",
            
           
"template": "your_app/dashboard/welcome_widget.html",
        })