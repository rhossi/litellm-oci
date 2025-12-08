"""
Example: Using OpenAI SDK with LiteLLM Proxy for OCI models

This demonstrates OpenAI API compatibility - you can use the standard OpenAI SDK
to call OCI models through the LiteLLM proxy.
"""

from openai import OpenAI


def load_models_from_api(client):
    """Load available models from LiteLLM proxy /v1/models endpoint"""
    models_response = client.models.list()
    models = [model.id for model in models_response.data]
    return models


def select_model(models, default="oci/xai.grok-3"):
    """Prompt user to select a model"""
    print("\nAvailable Models:")
    print("-" * 50)

    # Find default index
    default_index = None
    for i, model in enumerate(models, 1):
        if model == default:
            default_index = i
        print(f"{i}. {model}")

    print("-" * 50)

    # Get user input
    prompt = f"Select a model (1-{len(models)})"
    if default_index:
        prompt += f" [default: {default_index} - {default}]"
    prompt += ": "

    user_input = input(prompt).strip()

    # Handle default
    if not user_input and default_index:
        selected_index = default_index
    else:
        try:
            selected_index = int(user_input)
        except ValueError:
            print(f"Invalid input. Using default: {default}")
            selected_index = default_index if default_index else 1

    # Validate index
    if 1 <= selected_index <= len(models):
        return models[selected_index - 1]
    else:
        print(f"Invalid selection. Using default: {default}")
        return default if default in models else models[0]


def get_user_prompt(default="say hello from OCI"):
    """Prompt user for input message"""
    user_input = input(f"\nEnter your message [default: '{default}']: ").strip()
    return user_input if user_input else default


# Initialize OpenAI client pointing to LiteLLM proxy
# The proxy is running on http://localhost:4000
# Note: max_retries=0 to avoid OCI provider incompatibility
client = OpenAI(
    api_key="sk-any-string",  # Required by client but not validated by LiteLLM proxy
    base_url="http://localhost:4000/v1",  # LiteLLM proxy endpoint
    max_retries=0,  # OCI provider doesn't support max_retries parameter
)

# Load models from LiteLLM proxy API
print("Loading models from LiteLLM proxy (http://localhost:4000/v1/models)...")
try:
    models = load_models_from_api(client)
    if not models:
        print("⚠️  No models found from proxy. Using default: oci/xai.grok-3")
        selected_model = "oci/xai.grok-3"
    else:
        selected_model = select_model(models)
except Exception as e:
    print(f"⚠️  Error loading models from proxy: {e}")
    print(
        "   Make sure the LiteLLM proxy is running: python run_proxy.py --config config.yaml"
    )
    print("   Using default: oci/xai.grok-3")
    selected_model = "oci/xai.grok-3"

# Get user prompt
user_message = get_user_prompt()

# Make a chat completion request using OpenAI SDK
print("\n" + "=" * 50)
print(f"Making request to LiteLLM proxy using OpenAI SDK...")
print(f"Model: {selected_model}")
print(f"Message: {user_message}")
print("=" * 50)

try:
    response = client.chat.completions.create(
        model=selected_model,
        messages=[{"role": "user", "content": user_message}],
        temperature=0.7,
        max_tokens=150,
    )

    # Display the response in OpenAI format
    print(f"\n✅ Response from {response.model}:")
    print("-" * 50)
    print(response.choices[0].message.content)
    print("-" * 50)
    print(f"Usage: {response.usage}")
    print("✅ OpenAI API compatibility confirmed!")

except Exception as e:
    print(f"\n❌ Error: {e}")
    print("\nMake sure the LiteLLM proxy is running:")
    print("  python run_proxy.py --config config.yaml")
