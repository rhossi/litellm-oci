# LiteLLM OCI Proxy

A proxy server that provides **OpenAI API compatibility** for all models available through **OCI Generative AI**, including xAI Grok, Meta Llama, and Cohere models.

This proxy enables you to use the standard OpenAI SDK and API format to interact with OCI Generative AI models, making it easy to integrate OCI models into applications that expect OpenAI-compatible APIs.

## Setup

1. **Install dependencies:**
```bash
uv sync
```

2. **Create your configuration file:**
   - Copy the example configuration file:
   ```bash
   cp config.yaml.example config.yaml
   ```

3. **Configure OCI credentials:**
   - Open `config.yaml` in your editor
   - Replace the placeholder values with your OCI credentials:
     - `oci_user`: Your OCI user OCID
     - `oci_fingerprint`: Your OCI API key fingerprint
     - `oci_tenancy`: Your OCI tenancy OCID
     - `oci_region`: Your OCI region (e.g., `us-chicago-1`)
     - `oci_key_file`: Absolute path to your OCI API private key file (e.g., `/Users/yourname/.oci/oci_api_key.pem`)
     - `oci_compartment_id`: Your OCI compartment OCID
   
   **Note:** Use absolute paths for `oci_key_file` (the `~` tilde is not expanded by LiteLLM).

4. **Ensure your OCI API key is available:**
   - Make sure your OCI API private key file exists at the path specified in `oci_key_file`
   - The key file should have appropriate permissions (typically `600` or `400`)
   
   For help creating OCI API keys, see the [official Oracle tutorial](https://docs.oracle.com/en-us/iaas/Content/API/Concepts/apisigningkey.htm).

## Running the LiteLLM Proxy

Start the proxy server using the configuration file:

```bash
litellm --config config.yaml
```

The proxy will start on `http://localhost:4000` by default.

**Note**: If you're using Python 3.14 and encounter `uvloop` compatibility issues, use the wrapper script:

```bash
python run_proxy.py --config config.yaml
```

This wrapper script patches LiteLLM to use the `asyncio` event loop instead of `uvloop`, which is not compatible with Python 3.14.

## OpenAI API Compatibility

This proxy provides **full OpenAI API compatibility** for all OCI Generative AI models. You can use:

- **OpenAI Python SDK** - Drop-in replacement for OpenAI API calls
- OpenAI-compatible HTTP clients in any language
- Standard OpenAI API endpoints (`/v1/chat/completions`, `/v1/models`, etc.)
- OpenAI response format (same structure as OpenAI responses)

All OCI models are accessible through the standard OpenAI API interface, making it easy to switch between OpenAI and OCI models without changing your application code.

## Using the Proxy

### Python Example

```python
from openai import OpenAI

client = OpenAI(
    api_key="sk-any-string",  # Required by client but not validated by LiteLLM
    base_url="http://localhost:4000/v1"  # LiteLLM proxy endpoint
)

response = client.chat.completions.create(
    model="xai.grok-3",
    messages=[
        {"role": "user", "content": "Hello, how are you?"}
    ],
)

print(response.choices[0].message.content)
```

### cURL Example

```bash
curl http://localhost:4000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer sk-any-string" \
  -d '{
    "model": "xai.grok-3",
    "messages": [
      {"role": "user", "content": "Hello, how are you?"}
    ]
  }'
```

### Running the Example Script

The `main.py` file demonstrates OpenAI API compatibility by using the OpenAI SDK to call the LiteLLM proxy:

1. **First, start the proxy** (in one terminal):
```bash
python run_proxy.py --config config.yaml
```

2. **Then run the example** (in another terminal):
```bash
python main.py
```

The `main.py` script dynamically loads all available models from `config.yaml`, allows you to select a model interactively, and makes requests using the standard OpenAI SDK format. This demonstrates full OpenAI API compatibility for all OCI Generative AI models.

## Configuration

The `config.yaml` file (created from `config.yaml.example`) contains all supported OCI models with shared authentication credentials using YAML anchors. The configuration includes:

- **OCI authentication credentials** (user, fingerprint, tenancy, region, key file, compartment ID)
- **Region**: `us-chicago-1`
- **Serving mode**: `ON_DEMAND`
- **drop_params**: `true` (automatically filters unsupported parameters)

### Available Models

All supported OCI models are configured in `config.yaml`:

**xAI Grok Models:**
- `oci/xai.grok-4`
- `oci/xai.grok-4-fast-reasoning` (Reasoning mode - for complex, multi-step problems)
- `oci/xai.grok-4-fast-non-reasoning` (Non-Reasoning mode - for speed-critical queries)
- `oci/xai.grok-3`
- `oci/xai.grok-3-fast`
- `oci/xai.grok-3-mini`
- `oci/xai.grok-3-mini-fast`
- `oci/xai.grok-code-fast-1`

**Meta Llama Models:**
- `oci/meta.llama-4-maverick-17b-128e-instruct-fp8`
- `oci/meta.llama-4-scout-17b-16e-instruct`
- `oci/meta.llama-3.3-70b-instruct`
- `oci/meta.llama-3.2-90b-vision-instruct`
- `oci/meta.llama-3.1-405b-instruct`

**Cohere Models:**
- `oci/cohere.command-latest`
- `oci/cohere.command-a-03-2025`
- `oci/cohere.command-plus-latest`

To use a specific model, use its `model_name` when making requests (e.g., `oci/xai.grok-4`).

## Security Note

⚠️ **Important**: The `config.yaml` file contains sensitive credentials. Do not commit it to version control. Consider using environment variables or a secrets manager for production deployments.

