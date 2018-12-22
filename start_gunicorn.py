from app import app
import OCRFID

app.register_blueprint(OCRFID.blueprint)
