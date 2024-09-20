# Development

## Onvif Command Support
Each of the following Onvif Web services has its own directory:
- [Analytics](../analytics)
- [Device](../device)
- [Event](../event)
- [Imaging](../imaging)
- [Media](../media)
- [Media2](../media2)
- [PTZ](../ptz)

Inside each directory there is:
- `types.go`: contains the struct definitions for each onvif command and response
- `function.go`: contains the auto-generated types that implement the `Function` interface providing `Request()` and `Response()` type mappings.

At the root level there is:
- [names.go](../names.go): contains the auto-generated constant names of all the commands
- [mappings.go](../mappings.go): contains the auto-generated mappings for each Onvif WebService from function name to function datatype


### Adding support for additional commands
> **Note:** Currently, the python script looks for types that end with `Response` and work backwards from there.
> This is to prevent creating commands for every struct type defined there, and only the ones that are actually commands.
> It also skips any types ending with `FaultResponse`, as there typically are no `Fault` commands, only responses.

For the respective web service the command belongs to, add the command and response struct definitions
into `<web-service-name>/types.go`, and then run:
```shell
python3 python/gen_commands.py
```

> **Note:** You can also typically run the generator within your IDE thanks to the `//go:generate` lines 
> towards the top of the `types.go` files.


## WSDL 生成 req 和 resp

1. 安装 [gowsdl](https://github.com/hooklift/gowsdl)
2. cd /docs/wsdl
3. gowsdl xx.wsdl ，xx 替换为需要执行的 wsdl 文件，比如 media.wsdl
4. 默认生成在 docs/wsdl/myservice目录下
5. 在根目录下创建对应的 xx 目录，并将docs/wsdl/myservice/myservice.go 移动并重命名到 xx 目录，名字跟 xx 保持一致，比如 search/types.go
6. 修改 xx 的文件
7. 在 gen_commands.py SERVICE_NAMES 中添加配置
8. cd python
9. ./gen_commands.py
