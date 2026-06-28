from dotenv import load_dotenv

load_dotenv()

from graph.graph import graph

if __name__ == "__main__":
    state = {
        "stock": "RELIANCE.NS"
    }

    result = graph.invoke(state)

    print("\n🔥 FINAL OUTPUT:\n")
    print(result["recommendation"])