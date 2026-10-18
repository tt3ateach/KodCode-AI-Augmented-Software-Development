import test from 'node:test';
import assert from 'node:assert/strict';
import { createWorkItemsApiClient } from '../src/apiClient.js';
import { applyFilters, dueLabel, mapApiWorkItem } from '../src/state.js';
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

test('clearing a date sends explicit null',async()=>{
  let body;
  const client=createWorkItemsApiClient('',async(url,options)=>{
    body=JSON.parse(options.body);return {ok:true,status:200,json:async()=>({...item,due_date:null,overdue:false})};
  });
  await client.setDueDate('x','');
  assert.deepEqual(body,{due_date:null});
});
test('overdue filter uses the server flag and keeps exact IDs',()=>{
  const tasks=[mapApiWorkItem({...item,id:'past',due_date:'2026-10-03',overdue:true}),mapApiWorkItem({...item,id:'today',due_date:'2026-10-04',overdue:false})];
  assert.deepEqual(applyFilters(tasks,{status:'all',search:'',overdueOnly:true}).map(t=>t.id),['past']);
});
test('due labels follow the API flag and completion (REQ-08)',()=>{
  const base=mapApiWorkItem(item);
  assert.equal(dueLabel({...base,dueDate:'2026-10-03',overdue:true}),'Overdue');
  assert.equal(dueLabel({...base,status:'done',dueDate:'2026-10-03'}),'Done');
  assert.equal(dueLabel({...base,dueDate:'2026-10-04'}),'Due 2026-10-04');
  assert.equal(dueLabel(base),'No due date');
});
