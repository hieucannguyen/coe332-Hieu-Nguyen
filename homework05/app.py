from flask import Flask, request
from iss_tracker import get_data, find_closest_epoch, compute_speed

app = Flask(__name__)


@app.route("/epochs", methods=["GET"])
def get_epochs():
    """
        Route to return entire ISS dataset

        Query parameters:
            limit (int): limit amount of epochs
            offset (int): offset the epochs
    """
    data = get_data()
    limit = int(request.args.get("limit", 0))
    offset = int(request.args.get("offset", 0))
    if limit and offset:
        result = []
        for i in range(limit):
            result.append(data[offset + i])
        return result

    return data


@app.route("/epochs/<epoch>", methods=["GET"])
def get_specific_epoch(epoch):
    """
        Route to return a specific epoch in the ISS dataset

        Args:
            epoch (string): specific timestamp of the epoch
    """
    data = get_data()
    for item in data:
        if item["EPOCH"] == epoch:
            return item

    return "Epoch not found."


@app.route("/epochs/<epoch>/speed", methods=["GET"])
def get_specific_epoch_speed(epoch):
    """
        Route to return a specific epoch's speed in the ISS dataset

        Args:
            epoch (string): specific timestamp of the epoch
    """
    data = get_data()
    for item in data:
        if item["EPOCH"] == epoch:
            return {
                "EPOCH": item["EPOCH"],
                "Speed (km/s)": compute_speed(
                    float(item["X_DOT"]["#text"]),
                    float(item["Y_DOT"]["#text"]),
                    float(item["Z_DOT"]["#text"]),
                ),
            }

    return "Epoch not found."


@app.route("/now", methods=["GET"])
def get_current_epoch():
    """
        Route to return the closest epoch to the current time along with its speed in the ISS dataset

    """
    data = get_data()
    current_epoch = find_closest_epoch(data)
    current_epoch["Speed (km/s)"] = compute_speed(
        float(current_epoch["X_DOT"]["#text"]),
        float(current_epoch["Y_DOT"]["#text"]),
        float(current_epoch["Z_DOT"]["#text"]),
    )

    return current_epoch


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
