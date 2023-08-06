
const $ = require('jquery');

function navigator() {


    const GetQueryString = function (url, name, result) {
        let search = url;
        const resultCopy = result.concat();
        const reg = new RegExp('(^|&)' + name + '=([^&]*)(&|$)');
        const r = search.substring(search.indexOf('?')).substr(1).match(reg);
        const formdata = search.substring(search.indexOf('form_data=')).substr(10);
        if (r) {
            const target = decodeURI(r[2]);// decodeURI for Chinese url
            if (r !== null && target !== null && target !== '') {
                search = search.replace('&' + name + '=' + r[2], '');// replace source url
                resultCopy.push(target);
                return GetQueryString(search, name, resultCopy);
            } else {
                return resultCopy;
            }
        }
        else if (formdata && name !== 'standalone') {
            const target = JSON.parse(unescape(decodeURI(formdata)));
            if (target[name]) {
                return target[name];
            } else{
                return resultCopy;
            }
        }
        else {
            return resultCopy;
        }
    }

    // get slice by sliceId
    const sliceUrl = function (sliceId) {
        const navigateSlice = $.ajax({
            url: '/hand/rest/api/sliceUrl',
            async: false,
            data: { sliceId: sliceId },
            dataType: 'json',
        });
        return navigateSlice.responseText;
    }

    const dashboardUrl = function (title) {
        const navigateDashboard = $.ajax({
            url: '/hand/rest/api/dashboardUrl',
            async: false,
            data: {
                title: title,
            },
            type: 'POST',
            dataType: 'json',
        });
        return navigateDashboard.responseText;
    }

    const convertDashUrl = function (dash, groupby, clickTarget, groupbyValue, isFrozen) {
        let url = dash.url;
        //  &preselect_filters = {
        //   sliceId: {
        //     "groupby": [
        //       "filters"
        //       ],
        //     "groupby": [
        //       "filters"
        //       ]
        //     },
        //   sliceId: {
        //     "groupby": [
        //       "filters"
        //       ]
        //     }
        //   }
        const filter = {};
        for (let j = 0; j < dash.slcs.length; j++) {
            const filterId = dash.slcs[j].sliceId;
            const slc = {};
            // let slc = {};
            for (let i = 0; i < groupby.length; i++) {
                //   slc = {};
                const vals = [];
                const extCol = groupby[i];
                const val = (groupbyValue === null
                    ? clickTarget.parentNode.childNodes[i].textContent : groupbyValue[i]);
                for (let k = 0; k < dash.slcs[j].columns.length; k++) {
                    // make slice column equals dashboard filter column
                    if (extCol === dash.slcs[j].columns[k].extCol) {
                        // vals.push(val);
                        vals.push(val.toString());
                    }
                }
                //   slc[extCol] = vals;
                if (vals.length > 0) {
                    slc[extCol] = vals;
                }
            }
            filter[filterId] = slc;
        }
        url += '?preselect_filters=' + JSON.stringify(filter) + '&standalone=true&isControl=false&isManager=false';
        if (isFrozen) {
            url += '&frozenFilter=true';
        }
        return url;
    }


    // <!-- 模态框（Modal） -->
    // <div class="modal fade" id="myModal" tabindex="-1" role="dialog"
    //  aria-labelledby="myModalLabel" aria-hidden="true">
    // 	<div class="modal-dialog">
    // 		<div class="modal-content">
    // 			<div class="modal-header">
    // 				<button type="button" class="close" data-dismiss="modal" aria-hidden="true">
    // 					&times;
    // 				</button>
    // 				<h4 class="modal-title" id="myModalLabel">
    // 					模态框（Modal）标题
    // 				</h4>
    // 			</div>
    // 			<div class="modal-body">
    // 				在这里添加一些文本
    // 			</div>
    // 			<div class="modal-footer">
    // 				<button type="button" class="btn btn-default" data-dismiss="modal">关闭
    // 				</button>
    // 				<button type="button" class="btn btn-primary">
    // 					提交更改
    // 				</button>
    // 			</div>
    // 		</div><!-- /.modal-content -->
    // 	</div><!-- /.modal -->
    // </div>

    const handleNavigate = function (i, navigates) {
        // if (i === navigates.length - 1) {
            if (navigates.length === 1) {
                if (window.location.href.indexOf('isFrameIndex') === -1) {
                    window.postMessage(navigates[0], '*');
                } else {
                    window.parent.postMessage(navigates[0], '*');
                }
            } else if (navigates.length > 1) {
                const modal = document.createElement('div');
                modal.setAttribute('class', 'modal fade');
                // modal.style.marginTop = '100px';
                const modalDialog = document.createElement('div');
                modalDialog.setAttribute('class', 'modal-dialog');
                const modalHeader = document.createElement('div');
                modalHeader.setAttribute('class', 'modal-header');
                const modalTitle = document.createElement('h4');
                modalTitle.setAttribute('class', 'modal-title');
                modalTitle.style.textAlign = 'center';
                modalTitle.innerHTML = localMessage.choose_nav_target;
                const modalContent = document.createElement('div');
                modalContent.setAttribute('class', 'modal-content');
                const modalBody = document.createElement('div');
                modalBody.setAttribute('class', 'modal-body');
                for (let j = 0; j < navigates.length; j++) {
                    const item = document.createElement('div');
                    item.setAttribute('class', 'navWrapper');
                    // item.innerHTML = navigates[j].title;
                    const nav = document.createElement('div');
                    // nav.innerHTML = navigates[j].title;
                    nav.setAttribute('class', 'sim-button navItem');
                    const navInner = document.createElement('span');
                    navInner.innerHTML = navigates[j].title;
                    item.onclick = function () {
                        if (window.location.href.indexOf('isFrameIndex') === -1) {
                            window.postMessage(navigates[0], '*');
                        } else {
                            window.parent.postMessage(navigates[0], '*');
                        }
                        // window.parent.postMessage(navigates[j], '*');
                        $(modal).modal('hide');
                    };
                    nav.appendChild(navInner);
                    item.appendChild(nav);
                    modalBody.appendChild(item);
                }
                modalHeader.appendChild(modalTitle);
                modalContent.appendChild(modalHeader);
                modalContent.appendChild(modalBody);
                modalDialog.appendChild(modalContent);
                modal.appendChild(modalDialog);
                $(modal).modal('show');
            }
        // }
    }

    let left = 10;
    let startHeight;
    const isIE = (document.all) ? true : false;
    const Extend = function (destination, source) {
        for (const property in source) {
            destination[property] = source[property];
        }
    };
    const Bind = function (object, fun, args) {
        return function () {
            return fun.apply(object, args || []);
        };
    };
    const BindAsEventListener = function (object, fun) {
        const args = Array.prototype.slice.call(arguments).slice(2);
        return function (event) {
            return fun.apply(object, [event || window.event].concat(args));
        };
    };
    const CurrentStyle = function (element) {
        return element.currentStyle || document.defaultView.getComputedStyle(element, null);
    };
    function create(elm, parent, fn) {
        const element = document.createElement(elm);
        fn && fn(element);
        parent && parent.appendChild(element);
        return element;
    }
    function addListener(element, e, fn) {
        element.addEventListener ?
            element.addEventListener(e, fn, false) :
            element.attachEvent('on' + e, fn);
    }
    function removeListener(element, e, fn) {
        element.removeEventListener ?
            element.removeEventListener(e, fn, false) :
            element.detachEvent('on' + e, fn);
    }
    const Class = function (properties) {
        const eleClass = function () {
            return (arguments[0] !== null && this.init && typeof (this.init) === 'function') ?
                this.init.apply(this, arguments) : this;
        };
        eleClass.prototype = properties;
        return eleClass;
    };

    const Dialog = new Class({
        options: {
            Width: 300,
            Height: 300,
            Left: 100,
            Top: 100,
            Titleheight: 26,
            Minwidth: 200,
            Minheight: 200,
            CancelIco: true,
            ResizeIco: false,
            Info: '',
            Content: '',
            Zindex: 10,
            IsDash: false,
        },
        init: function (options) {
            this.optDragobj = null;
            this.optResize = null;
            this.optCancel = null;
            this.optBody = null;
            this.optX = 0;
            this.optY = 0;
            this.optFM = BindAsEventListener(this, this.Move);
            this.optFS = Bind(this, this.Stop);
            this.optIsdrag = null;
            this.optCss = null;
            this.Width = this.options.Width;
            this.Height = this.options.Height;
            this.Left = this.options.Left;
            this.Top = this.options.Top;
            this.CancelIco = this.options.CancelIco;
            this.Info = this.options.Info;
            this.Content = this.options.Content;
            this.Minwidth = this.options.Minwidth;
            this.Minheight = this.options.Minheight;
            this.Titleheight = this.options.Titleheight;
            this.Zindex = this.options.Zindex;
            this.IsDash = this.options.IsDash;
            Extend(this, options);
            Dialog.Zindex = this.Zindex;
            // 构造dialog
            const obj = ['dialogcontainter', 'dialogtitle', 'dialogtitleinfo', 'dialogtitleico',
                'dialogbody', 'dialogbottom'];
            for (let i = 0; i < obj.length; i++) {
                obj[i] = create('div', null, function (e) {
                    const elm = e;
                    elm.className = obj[i];
                    return elm;
                });
            }
            obj[2].innerHTML = this.Info;
            obj[4].innerHTML = this.Content;
            obj[1].appendChild(obj[2]);
            obj[1].appendChild(obj[3]);
            obj[0].appendChild(obj[1]);
            obj[0].appendChild(obj[4]);
            obj[0].appendChild(obj[5]);
            document.body.appendChild(obj[0]);
            this.optDragobj = obj[0];
            this.optResize = obj[5];
            this.optCancel = obj[3];
            this.optBody = obj[4];
            // o,x1,x2
            // 设置Dialog的长 宽 ,left ,Top
            // with(this._dragobj.style){
            //      height = this.Height + "px";top = this.Top + "px";width = this.Width +"px";
            //      left = this.Left + "px";zIndex = this.Zindex;
            // }
            this.optDragobj.style.height = this.Height + 'px';
            this.optDragobj.style.top = this.Top + 'px';
            this.optDragobj.style.width = this.Width + 'px';
            this.optDragobj.style.left = this.Left + 'px';
            this.optDragobj.style.zIndex = this.Zindex;
            this.optBody.style.height = this.Height
                - this.Titleheight - parseInt(CurrentStyle(this.optBody).paddingLeft) * 2 + 'px';
            // 添加事件
            addListener(this.optDragobj, 'mousedown', BindAsEventListener(this, this.Start, true));
            addListener(this.optCancel, 'mouseover', Bind(this, this.Changebg,
                [this.optCancel, '0px 0px', '-21px 0px']));
            addListener(this.optCancel, 'mouseout', Bind(this, this.Changebg,
                [this.optCancel, '0px 0px', '-21px 0px']));
            addListener(this.optCancel, 'mousedown', BindAsEventListener(this, this.Disappear));
            addListener(this.optBody, 'mousedown', BindAsEventListener(this, this.Cancelbubble));
            addListener(this.optResize, 'mousedown', BindAsEventListener(this, this.Start, false));
        },
        Disappear: function (e) {
            this.Cancelbubble(e);
            document.body.removeChild(this.optDragobj);
        },
        Cancelbubble: function (e) {
            this.optDragobj.style.zIndex = ++Dialog.Zindex;
            document.all ? (e.cancelBubble = true) : (e.stopPropagation());
        },
        Changebg: function (o, x1, x2) {
            o.style.backgroundPosition = (o.style.backgroundPosition === x1) ? x2 : x1;
        },
        Start: function (e, isdrag) {
            startHeight = this.optBody.style.height;
            if (!isdrag) {
                this.Cancelbubble(e);
            }
            this.optCss = isdrag ? { x: 'left', y: 'top' } : { x: 'width', y: 'height' };
            this.optDragobj.style.zIndex = ++Dialog.Zindex;
            this.optIsdrag = isdrag;
            this.optX = isdrag ? (e.clientX - this.optDragobj.offsetLeft || 0) :
                (this.optDragobj.offsetLeft || 0);
            this.optY = isdrag ? (e.clientY - this.optDragobj.offsetTop || 0) :
                (this.optDragobj.offsetTop || 0);
            if (isIE) {
                addListener(this.optDragobj, 'losecapture', this.optFS);
                this.optDragobj.setCapture();
            } else {
                e.preventDefault();
                addListener(window, 'blur', this.optFS);
            }
            addListener(document, 'mousemove', this.optFM);
            addListener(document, 'mouseup', this.optFS);
        },
        Move: function (e) {
            window.getSelection ? window.getSelection().removeAllRanges() :
                document.selection.empty();
            const iX = e.clientX - this.optX;
            const iY = e.clientY - this.optY;
            this.optDragobj.style[this.optCss.x] = (this.optIsdrag ? Math.max(iX, 0) :
                Math.max(iX, this.Minwidth)) + 'px';
            this.optDragobj.style[this.optCss.y] = (this.optIsdrag ? Math.max(iY, 0) :
                Math.max(iY, this.Minheight)) + 'px';
            if (!this.optIsdrag) {
                this.optBody.style.height = Math.max(iY - this.Titleheight,
                    this.Minheight - this.Titleheight) -
                    2 * parseInt(CurrentStyle(this.optBody).paddingLeft) + 'px';
            }
        },
        Stop: function () {
            removeListener(document, 'mousemove', this.optFM);
            removeListener(document, 'mouseup', this.optFS);
            // if target is Slice, change area will redraw
            if (!this.IsDash) {
                if (startHeight !== this.optBody.style.height) {
                    const frame = this.optBody.childNodes[0];
                    let newUrl = frame.getAttribute('src');
                    const navHeight = GetQueryString(newUrl, 'navHeight', []);
                    if (navHeight.length !== 0) {
                        newUrl = newUrl.replace('navHeight=' + navHeight,
                            'navHeight=' + this.optBody.style.height);
                    } else {
                        newUrl += '&navHeight=' + this.optBody.style.height;
                    }
                    frame.setAttribute('src', newUrl);
                }
            }
            if (isIE) {
                removeListener(this.optDragobj, 'losecapture', this.optFS);
                this.optDragobj.releaseCapture();
            } else {
                removeListener(window, 'blur', this.optFS);
            }
        },
    });
    function createModal(title, url, height, width, isDash) {
        let modals;
        if ($('#modals').attr('id') !== undefined) {
            modals = $('#modals');
        } else {
            modals = document.createElement('div');
            $(modals).attr('id', 'modals');
            document.body.append(modals);
        }
        const modalCount = $('#modals').children().length;
        const navHeight = height - 26 - 20 + 'px';
        let newUrl = url + '&isFrameIndex=false';
        let content = '';
        if (isDash) {
            newUrl += '&standalone=true';
            content = '<iframe id = "newSlice_' + modalCount +
                '" width = "100%" height = "100%" scrolling = "auto" frameBorder = "0" src = ' +
                newUrl + '> </iframe>';
        } else {
            newUrl += '&navHeight=' + navHeight;
            content = '<iframe id = "newSlice_' + modalCount +
                '" width = "100%" height = "100%" scrolling = "no" frameBorder = "0" src = "' +
                newUrl + '"> </iframe>';
        }
        new Dialog({
            Url: newUrl,
            Height: height,
            Width: width,
            Info: title,
            Left: 300 + left,
            Top: 100,
            Content: content,
            Zindex: (++Dialog.Zindex),
            IsDash: isDash,
        });
        left += 10;
    }

    // add listener to get navigate message
    $(document).ready(function () {
        window.onmessage = function (e) {
            if (e.data.type === 'new window') {
                window.open(e.data.url, null, null);
            } else {
                // make modal can be add only once
                // if ($('#newSlice_' + count).attr('id') === undefined) {
                //     // showModal(e.data.title, e.data.url);
                //     createModal(e.data.title, e.data.url, e.data.navHeight, e.data.navWidth, e.data.isDash);
                //     count++;
                // }
                if (e.data.isDash){
                    e.data.url = encodeURI(e.data.url)
                }
                top.layer.open({
                    type: 2,
                    title: e.data.title,
                    maxmin: true,
                    shadeClose: true, //点击遮罩关闭层
                    shade: 0,
                    area: [e.data.navWidth, e.data.navHeight],
                    content: [e.data.url],
                    // offset: [ //为了演示，随机坐标
                    //     // Math.random() * ($(window).height() - 300)
                    //     $(window).height()/2
                    //     , Math.random() * ($(window).width() - 390)
                    // ],
                    btn: ['全部关闭'],
                    yes: function (index, layero) {
                        // top.layer.close(index);
                        top.layer.closeAll();
                    }
                });
            }
        };
    });

    // add filter by change url
    const addFilter = function (url, sourceGroupby, navGroupby, clickTarget, groupbyValue) {
        let newUrl = url;
        const formdata = url.substring(newUrl.indexOf('form_data=')).substr(10);
        const target = JSON.parse(unescape(decodeURI(formdata)));
        if (navGroupby.length > 0) {
            for (let j = 0; j < sourceGroupby.length; j++) {
                const val = (groupbyValue === null ? clickTarget.parentNode.childNodes[j].textContent : groupbyValue[j]);
                for (let k = 0; k < navGroupby.length; k++) {
                    // make navigate groupby val equals source groupby
                    if (sourceGroupby[j] === navGroupby[k]) {
                        const flt = newUrl.match(/flt_col/g);
                        let nextFltIndex = 0;
                        if (flt === null || flt === '') {
                            nextFltIndex = 1;
                        } else {
                            nextFltIndex = flt.length + 1;
                        }
                        const col = sourceGroupby[j];
                        // const nextFlt = '&flt_col_' + nextFltIndex + '=' + col + '&flt_op_' + nextFltIndex +
                        //     '=in&flt_eq_' + nextFltIndex + '=' + val;
                        // newUrl += nextFlt;
                        // "filters":[{"col":"string2","op":"in","val":["1"]}]
                        target['filters'].push({
                            "col": col,
                            "op": 'in',
                            "val": [val]
                        });
                    }
                }
            }
        }
        newUrl = newUrl.substring(0, newUrl.indexOf('form_data='));
        newUrl += 'form_data=' + JSON.stringify(target);
        return encodeURI(newUrl);
    }
    return {
        dashboardUrl: dashboardUrl,
        convertDashUrl: convertDashUrl,
        sliceUrl: sliceUrl,
        GetQueryString: GetQueryString,
        addFilter: addFilter,
        handleNavigate: handleNavigate,
    };
}




module.exports = navigator;
