biocloud = {
    addDefaultProgramTo: function(container){
        
        var number = $("div.program", container).size();
        var thisProgram = $('<div class="program" id="program'+number+'"></div>')
            .insertBefore($('div.submitButtons', container));
        var programParameters = document.createElement("ul");
        programParameters.className = "parameters";
        
        thisProgram.append('<div class="removeProgram"><a>-</a></div>');
        $('.removeProgram a', thisProgram)
            .click(function(event){ thisProgram.remove();
                                    event.preventDefault()});
        thisProgram.append("Select Program ");
        thisProgram.append(this.programSelectorFor($(programParameters), number));
        thisProgram.append(programParameters);
    },
    createProgramSelectorFor: function(somePrograms){
        var programSelector = $(document.createElement("select"));
        programSelector.append("<option>&lt;Select Program&gt;</option>")
        jQuery.each(somePrograms, function(i, each){
            programSelector.append("<option>" + each.name + "</option>")
        });
        this.programSelector = programSelector;
    },
    fillWithFileNames: function(aSelectNode){
        aSelectNode.empty();
        aSelectNode.append('<option value="">----------&gt;</option>');
        jQuery.each(this.fileNames, function(i, each){
            aSelectNode.append("<option>"+each+"</option>")
        });
    },
    fillWithFiles: function(ulTag){
    	if (ulTag != null){
    		ulTag.innerHTML = "";
    		jQuery.each(this.fileNames, function(i, each){
    			ulTag.innerHTML += "<li>"+each+"</li>"
            });
    	}
    },
    programSelectorFor: function(aProgramParameterBox, sequenceNumber){
        var programSelector = $(this.programSelector).clone();
        programSelector.attr("name", "program."+sequenceNumber+".programName");
        programSelector.change(function(event){
            biocloud.updateProgramBoxFor(aProgramParameterBox,
                event.target.value, sequenceNumber)
        });
        return programSelector;
    },
    setPrograms: function(anArrayOfProgramSpecs){
        this.programSpecs = anArrayOfProgramSpecs;
        this.programs = jQuery.map(anArrayOfProgramSpecs, function(each){
            return new biocloud.Program(each);
        })
        this.createProgramSelectorFor(this.programs)
    },
    setFiles: function(anArrayOfFileNames){
        this.fileNames = anArrayOfFileNames.sort();
        biocloud.fillWithFiles($("#uploaded-files-id")[0])
        $('select.file').each(function(i, each){
            var select = $(each);
            var input = select.next("input[type=text]");
            if(select.val() != "" && input.val() == ""){
                input.val(select.val());
            }
            biocloud.fillWithFileNames(select);
        });
        
    },
    updateProgramBoxFor: function(aProgramBox, aProgramName, sequenceNumber){
        var program = undefined;
        jQuery.each(biocloud.programs, function(i, each){
            if(each.name == aProgramName){
                program = each;
                return false;
            }
        });
        aProgramBox.empty()
        if(program !== undefined) program.renderTo(aProgramBox, sequenceNumber);
    },
    workflow: {},

    // Class constructor functions (their prototypes follow after
    // the biocloud object)
    Program: function(aProgramSpec){
        this.name = aProgramSpec.name;
        this.homepage = aProgramSpec.homepage;
        this.files = [];
        for(i=0; i < aProgramSpec.inputs; i++){
            this.files
                .push(new biocloud.InputFile(i,
                        aProgramSpec.fileNames[i]));
        }
        for(i=0; i < aProgramSpec.outputs; i++){
            this.files
                .push(new biocloud.OutputFile(i+1, aProgramSpec.inputs + i,
                        aProgramSpec.fileNames[aProgramSpec.inputs + i]));
        }
        /* What to do about parameters? */
    },
    InputFile: function(index, name){
        this.index = index+1;
        this.name = name;
        this.fieldIndex = index;
    },
    OutputFile: function(index, fieldIndex, name){
        this.index = index;
        this.name = name;
        this.fieldIndex = fieldIndex;
    }
};

biocloud.Program.prototype = {
    renderTo: function(aBox, id){
        aBox.append('<li class="homepage"><a href="'+this.homepage+'">Homepage</li>')
        aBox.append("Select file(s)")
        jQuery.each(this.files, function(i, each){
            each.renderTo($("<li></li>").appendTo(aBox), id)
        })
        this.command = $('<input type="text" class="commandline" readonly="readonly" name="program.'+id+'.commandPreview" />')
            .appendTo($("<li></li>")
                .appendTo(aBox));
    }
};
// create a block context, to avoid cluttering the global namespace with the fileprototype
(function (){
    var fileprototype = {
        renderTo: function(aBox, id){
            var name = 'program.'+id+'.file.'+this.fieldIndex;
            aBox.append(this.index + ". " + this.name + '<br />'+
                '<select name="'+name+'.select" class="file"></select>'+
                '<input type="text" class="file" name="'+name+'.input"/>');
            var select = $('select.file', aBox),
                input = $('input.file', aBox);
            biocloud.fillWithFileNames(select);
            input.change(function(event){
                select.attr('value', "");
            });
            select.change(function(event){
                input.attr('value', '');
            });
        }
    };
    biocloud.InputFile.prototype = fileprototype;
    biocloud.OutputFile.prototype = fileprototype;
})();

$(document).ready(function(event){
    // basic setting of biocloud variables
    biocloud.workflow = $("form#workflow");
    biocloud.addDefaultProgramTo(biocloud.workflow);
    
    $("a#addProgram").click(function(event){
        biocloud.addDefaultProgramTo(biocloud.workflow)
        event.preventDefault();
    });

    // add XHR requesting to avoid losing the other form/inputs
    $('form#newProject').submit(function(event){
        event.preventDefault();
        var form = $(this),
            values = {};
        form.find('input').each(function(i, each){
                values[each.name] = each.value;
            });
        $.post(form.attr('action'), values, function(data){
            if(data == values.projectName){
                $("select.project").first().prepend(
                    '<option selected="selected">'+values.projectName+'</option>')
            } else {
                alert(data);
            }
        })
    });
    
    // update of available files
    $('select.project').first().change(function(event){
        event.preventDefault();
        if (this.value == '') {// no selected project
        	 biocloud.setFiles([]);
        } else {
	        $.getJSON('/xhr/'+this.value+'/content', function(data){
	            biocloud.setFiles(data);
	        });
        }
    });
});
