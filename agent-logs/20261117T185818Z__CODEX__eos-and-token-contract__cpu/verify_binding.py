"""Verify static EOS correction binding without loading a tokenizer or model."""
import hashlib
import json
from pathlib import Path


def read_bound(item):
    raw=Path(item['path']).read_bytes()
    if hashlib.sha256(raw).hexdigest()!=item['sha256']:
        raise ValueError('digest mismatch: '+item['path'])
    return raw


binding=json.loads((Path(__file__).parent/'eos_binding_candidate.json').read_text())
if binding['schema']!='FORWARD_EOS_CONTRACT_CORRECTION_CANDIDATE_V1':raise ValueError('schema')
old=json.loads(read_bound(binding['original_plan']))['inference_contract']
refs=binding['bound_static_files']
data={key:read_bound(value) for key,value in refs.items()}
tokenizer=json.loads(data['tokenizer_config']); generation=json.loads(data['generation_config'])
corrected=binding['forward_correction']
if old['tokenizer_eos_id']!=binding['original_plan']['old_primary_eos_id']:
    raise ValueError('old plan field differs')
if old['allowed_generation_eos_ids']!=corrected['model_generation_stop_ids'] or old['pad_token_id']!=corrected['pad_id']:
    raise ValueError('unrelated old plan fields differ')
if tokenizer['eos_token']!=corrected['primary_tokenizer_eos_token'] or tokenizer['pad_token']!=corrected['pad_token']:
    raise ValueError('token names')
decoder=tokenizer['added_tokens_decoder']
for ident,token in ((corrected['primary_tokenizer_eos_id'],tokenizer['eos_token']),
                    (corrected['pad_id'],tokenizer['pad_token'])):
    if decoder[str(ident)]['content']!=token:raise ValueError('token id mapping')
if generation['eos_token_id']!=corrected['model_generation_stop_ids'] or generation['pad_token_id']!=corrected['pad_id']:
    raise ValueError('generation static config')
if generation.get('forced_eos_token_id') is not None or old['forced_eos_token_id'] is not None:
    raise ValueError('forced eos not null')
if corrected['primary_tokenizer_eos_id']==corrected['pad_id']:
    raise ValueError('primary eos equals pad')
if corrected['accepted_final_nonpad_producer_eos_ids']!=[corrected['primary_tokenizer_eos_id']]:
    raise ValueError('nonpad producer eos')
if corrected['pad_id'] not in corrected['model_generation_stop_ids']:
    raise ValueError('expected model stop/pad overlap absent')
if (corrected['actor_output_padding_disposition']!='POLICY_FAILURE_OUTPUT_PADDING' or
    corrected['intermediate_generation_stop_disposition']!='POLICY_FAILURE_EARLIER_EOS' or
    corrected['secondary_stop_equal_to_pad_is_not_valid_actor_termination'] is not True):
    raise ValueError('frozen actor disposition differs')
print(json.dumps({'status':'STATIC_BINDING_PASS','source_file_count':len(data)+1,
                  'old_primary_eos':old['tokenizer_eos_id'],
                  'corrected_primary_eos':corrected['primary_tokenizer_eos_id'],
                  'model_stop_ids':corrected['model_generation_stop_ids'],'pad_id':corrected['pad_id'],
                  'forced_eos_explicit_in_static_generation_config':'forced_eos_token_id' in generation,
                  'runtime_observation':binding['runtime_observation'],
                  'science_authorization':binding['scientific_execution_authorization']},sort_keys=True))
