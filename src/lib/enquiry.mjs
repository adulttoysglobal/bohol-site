export function buildEnquiry(fields,models){
 const text=value=>String(value??'').trim();
 return ['PRODUCT ENQUIRY',`Prepared: ${new Date().toISOString().slice(0,10)}`,'',`Name: ${text(fields.name)}`,`Company: ${text(fields.company)}`,`Email: ${text(fields.email)}`,`Market: ${text(fields.market)}`,`Enquiry type: ${text(fields.type)}`,`Expected quantity: ${text(fields.quantity)}`,'','SELECTED PRODUCTS',...(models.length?models.map(m=>`- ${text(m)}`):['No specific model selected']),'','REQUIREMENTS',text(fields.message),'','This brief is an enquiry, not an order or an agreed quotation.'].join('\n');
}
