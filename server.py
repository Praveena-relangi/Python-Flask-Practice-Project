from flask import Flask, render_template, request, jsonify
from SentimentAnalysis.sentiment_analysis import sentiment_analyzer

# Initialize the Flask app
app = Flask("Sentiment Analyzer", static_folder="static")

@app.route("/")
def render_index_page():
    """
    Renders the main HTML page.
    """
    return render_template('index.html')

@app.route("/sentimentAnalyzer")
def sent_analyzer():
    """
    Handles AJAX requests for sentiment analysis.
    Accepts the text to be analyzed as a query parameter.
    """
    # Retrieve the text to analyze from the query parameter
    text_to_analyze = request.args.get('textToAnalyze')

    if not text_to_analyze:
        return jsonify({"error": "No text provided"}), 400

    # Perform sentiment analysis
    response = sentiment_analyzer(text_to_analyze)

    # Handle errors in sentiment analysis
    if "error" in response:
        return jsonify({"error": response['error']}), 500

    # Return the label and score as a JSON response
    return jsonify({
        "label": response['label'],
        "score": response['score']
    })

if __name__ == "__main__":
    """
    Executes the Flask app and deploys it on localhost:5000.
    """
    app.run(host="0.0.0.0", port=5000)
