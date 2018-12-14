from app import app
import ocrfid

app.register_blueprint(ocrfid.blueprint)
