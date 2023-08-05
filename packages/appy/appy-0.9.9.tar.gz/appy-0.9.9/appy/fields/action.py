# Copyright (C) 2007-2017 Gaetan Delannay

# This file is part of Appy.

# Appy is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Appy is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with Appy. If not, see <http://www.gnu.org/licenses/>.

# ------------------------------------------------------------------------------
import os.path
from appy.fields import Field, Layouts
from appy.px import Px
from appy.shared import utils as sutils

# ------------------------------------------------------------------------------
class Action(Field):
    '''An action is a Python method that can be triggered by the user on a
       given gen-class. An action is rendered as a button.'''

    # PX for viewing the Action button
    pxView = pxCell = Px('''
     <form var="formId='%s_%s_form' % (zobj.id, name);
                label=_(field.labelId);
                inputTitle=field.getInputTitle(zobj, label);
                inputLabel=field.getInputLabel(label, layoutType);
                smallButtons=smallButtons|False;
                css=ztool.getButtonCss(label, smallButtons, field.render);
                back=(layoutType == 'cell') and q(zobj.id) or 'null'"
           id=":formId" action=":zobj.absolute_url() + '/onExecuteAction'"
           style="display:inline">
      <input type="hidden" name="fieldName" value=":name"/>
      <input type="hidden" name="popupComment" value=""/>
      <input type="button" class=":css" title=":inputTitle"
         var="textConfirm=field.getConfirmText(_);
              showComment=(field.confirm == 'text') and 'true' or 'false'"
         value=":inputLabel" style=":url(field.icon, bg=True)"
         onclick=":'submitForm(%s,%s,%s,%s)' % (q(formId), q(textConfirm), \
                                                showComment, back)"/>
     </form>''')

    # It is not possible to edit an action, not to search it
    pxEdit = pxSearch = ''

    def __init__(self, validator=None, multiplicity=(1,1), default=None,
                 show=('view', 'result'), page='main', group=None, layouts=None,
                 move=0, specificReadPermission=False,
                 specificWritePermission=False, width=None, height=None,
                 maxChars=None, colspan=1, action=None, result='computation',
                 downloadDisposition='attachment', confirm=False, master=None,
                 masterValue=None, focus=False, historized=False, mapping=None,
                 label=None, icon=None, view=None, cell=None, xml=None,
                 render='button'):
        # Can be a single method or a list/tuple of methods
        self.action = action
        # For the 'result' param:
        #  * value 'computation' means that the action will simply compute
        #    things and redirect the user to the same page, with some status
        #    message about execution of the action;
        #  * 'file' means that the result is the binary content of a file that
        #    the user will download (it must be an opened Python file handler;
        #    after the action has been executed, Appy will close the handler);
        #  * 'redirect' means that the action will lead to the user being
        #    redirected to some other page.
        self.result = result
        # If self.result is "file", the "disposition" for downloading the file
        # is defined in self.downloadDisposition and can be "attachment" or
        # "inline".
        self.downloadDisposition = downloadDisposition
        # If following field "confirm" is True, a popup will ask the user if
        # she is really sure about triggering this action.
        self.confirm = confirm
        # If no p_icon is specified, "action.png" will be used
        self.icon = icon or 'action'
        Field.__init__(self, None, (0,1), default, show, page, group, layouts,
                       move, False, True, None, False, specificReadPermission,
                       specificWritePermission, width, height, None, colspan,
                       master, masterValue, focus, historized, mapping, label,
                       None, None, None, None, False, False, view, cell, xml)
        self.validable = False
        # There are various wways to render the action in the ui:
        # "button"   (the default) as a button;
        # "icon"     as an icon on layouts where compacity is a priority
        #            (ie, within lists of objects) but still as a button on the
        #            "view" layout.
        self.render = render

    def getDefaultLayouts(self): return Layouts.Action.b

    def renderLabel(self, layoutType):
        return # Label is rendered directly within the button

    def callAction(self, obj, method, hasParam, param):
        '''Calls p_method on p_obj. m_method can be the single action as defined
           in self.action or one of them is self.action contains several
           methods. Calling m_method can be done with a p_param (when p_hasParam
           is True), ie, when self.confirm is "text".'''
        if hasParam: return method(obj, param)
        else: return method(obj)

    def __call__(self, obj):
        '''Calls the action on p_obj'''
        # Must we call the method(s) with a param ?
        hasParam = self.confirm == 'text'
        param = hasParam and obj.request.get('popupComment', None)
        if type(self.action) in sutils.sequenceTypes:
            # There are multiple methods
            res = [True, '']
            for act in self.action:
                actRes = self.callAction(obj, act, hasParam, param)
                if type(actRes) in sutils.sequenceTypes:
                    res[0] = res[0] and actRes[0]
                    if self.result.startswith('file'):
                        res[1] = res[1] + actRes[1]
                    else:
                        res[1] = res[1] + '\n' + actRes[1]
                else:
                    res[0] = res[0] and actRes
        else:
            # There is only one method
            actRes = self.callAction(obj, self.action, hasParam, param)
            if type(actRes) in sutils.sequenceTypes:
                res = list(actRes)
            else:
                res = [actRes, '']
        # If res is None (ie the user-defined action did not return anything),
        # we consider the action as successfull.
        if res[0] == None: res[0] = True
        return res

    def isShowable(self, obj, layoutType):
        if layoutType == 'edit': return
        return Field.isShowable(self, obj, layoutType)

    def getInputTitle(self, obj, label):
        '''Returns the content of attribute "title" for the "input" field
           corresponding to the action in the ui.'''
        if not self.hasDescr: return label
        return '%s: %s' % (label, obj.translate(self.descrId))

    def getInputLabel(self, label, layoutType):
        '''Returns the label to display on the button corresponding to this
           action = the content of attribute "value" for the "input" field.'''
        # An icon is a button rendered without "value", excepted on the "view"
        # layout, where we still display it.
        if (self.render == 'icon') and (layoutType != 'view'): return ''
        return label

    def getConfirmText(self, _):
        '''Get the text to display in the confirm popup'''
        if not self.confirm: return ''
        return _(self.labelId + '_confirm', blankOnError=True) or \
               _('action_confirm')

    # Action fields can a priori be shown on every layout, "buttons" included
    def isRenderable(self, layoutType): return True

    def onUiRequest(self, obj, rq):
        '''This method is called when a user triggers the execution of this
           action from the user interface.'''
        # Execute the action (method __call__)
        actionRes = self(obj.appy())
        # Unwrap action results
        successfull, msg = actionRes
        if not msg:
            # Use the default i18n messages
            suffix = successfull and 'done' or 'ko'
            msg = obj.translate('action_%s' % suffix)
        if (self.result == 'computation') or not successfull:
            # If we are called from an Ajax request, simply return msg
            if hasattr(rq, 'pxContext') and rq.pxContext['ajax']: return msg
            obj.say(msg)
            return obj.goto(obj.getUrl(obj.getReferer()))
        elif self.result == 'file':
            # msg does not contain a message, but a Python file handler
            response = rq.RESPONSE
            response.setHeader('Content-Type', sutils.getMimeType(msg.name))
            response.setHeader('Content-Disposition', '%s;filename="%s"' % \
                         (self.downloadDisposition, os.path.basename(msg.name)))
            response.write(msg.read())
            msg.close()
        elif self.result == 'redirect':
            # msg does not contain a message, but the URL where to redirect
            # the user. Redirecting is different if we are in an Ajax request.
            if hasattr(rq, 'pxContext') and rq.pxContext['ajax']:
                rq.RESPONSE.setHeader('Appy-Redirect', msg)
                obj.setMessageCookie()
            else:
                return obj.goto(msg)
# ------------------------------------------------------------------------------
