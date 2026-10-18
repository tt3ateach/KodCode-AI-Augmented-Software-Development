import test from 'node:test';
import assert from 'node:assert/strict';
import { createWorkItemsApiClient } from '../src/apiClient.js';
import { applyFilters, mapApiWorkItem } from '../src/state.js';
const item={id:'x',title:'Test',status:'todo',priority:'medium',created_at:'2026-10-03T12:00:00Z'};
test('API status maps to the existing frontend status',()=>assert.equal(mapApiWorkItem({...item,status:'in_progress'}).status,'in-progress'));
test('service seam supports completion and reopening',async()=>{
  const calls=[];
  const client=createWorkItemsApiClient('',async(url,options)=>{
    calls.push([url,options]);return {ok:true,status:200,json:async()=>item};
  });
  await client.toggleDone('x');
  assert.equal(calls.length,2);
  assert.deepEqual(JSON.parse(calls[1][1].body),{status:'done'});
});
test('status filter preserves exact task membership',()=>{
  assert.deepEqual(applyFilters([mapApiWorkItem(item),mapApiWorkItem({...item,id:'done',status:'done'})],{status:'done',search:''}).map(t=>t.id),['done']);
});
