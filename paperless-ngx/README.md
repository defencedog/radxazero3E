# Paperless-ngx & Syncthing for Engineering Books, Notes & LinkedIN articles (WIP...)

## While in CasaOS
Install using *sqlite* database to make it less resource hungry. Recall we are using RK3566 CPU with 4Gb RAM. I use document indexer *sist2* along with *paperless-ngx* & both are resource-hungry. Thus following x2 `*.yaml` in my case are working together otherwise following errors happen

> Resource not available...
>
> new thread cannot be created...

To remove above errors also try [solution-1](https://github.com/defencedog/radxazero3E/blob/main/CasaOS_Docker_Container_Bug.md#solution-1)

- [paperless-ngx with sqlite](https://github.com/defencedog/radxazero3E/blob/main/CasaOS_yaml/Paperless-ngx-sqlite.yaml)
- [sist2 with less resources](https://github.com/defencedog/radxazero3E/blob/main/CasaOS_yaml/sist2_less_resource.yaml)

If you want to index some directory its better to nudge *sist2* configurations to match [this](https://github.com/defencedog/radxazero3E/blob/main/CasaOS_yaml/sist2.yaml) & temporarily disable *paperless-ngx*

## While in Paperless-ngx
### OCR
Our purpose is to allow some time to resource-intensive OCR process before echoing some error & skipping file altogether
> Configuration (side panel) > OCR
- enable Deskew
- disable Rotate page
- In OCR arguments write

```
{"invalidate_digital_signatures": true, "tesseract_timeout": 180, "jobs": 2, "continue_on_soft_render_error": true}
```
### Tags
Our purpose is to assign `uncategorized` tag to all freshly added documents which user afterwards can tag 
> Tags (side panel) > Create
- New tag name `uncategorized`
- enable check *inbox tag*
### Dashboard Custom View
In conjunction with the above. Dashboard landing page (homepage) can further be customised
> Documents (side panel) > Tags (filter `uncategorized`) > View (Save as) > check Dashboard
>
> Dashboard (side panel) > Homepage will have all documents user need to classify properly

**Tip** 
If you plan to upload say 10 books about Python programming which share same tags. You can enable check *inbox tag* for those tags. Then upload all documents at once! 
