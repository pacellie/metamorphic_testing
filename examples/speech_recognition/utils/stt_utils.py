import torch

__all__ = ['stt_read_audio', 'stt_prepare_audio']

_, _, (_, _, stt_read_audio, stt_prepare_audio) = torch.hub.load(
    repo_or_dir='snakers4/silero-models',
    model='silero_stt',
    language='en',  # also available 'de', 'es'
    device=torch.device('cpu')
)
