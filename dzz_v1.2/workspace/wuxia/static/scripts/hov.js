$(function(){
  var $lycon=$(".lycon1");
  var $txt=$(".lycon1").text();
      $lycon.focus(function(){
		  var $lytxt=$(this).text();
		  if($lytxt==$txt){
			  $(this).text("");
			  }
		  
		  })
	  $lycon.blur(function(){
		  var $lytxt=$(this).text();
		  if($lytxt==""){
			  $(this).text($txt);
			  }
		  })
})
$(function(){
	var $lycon1=$(".zsname");
  var $txt1=$(".zsname").val();
      $lycon1.focus(function(){
		  var $lytxt1=$(this).val();
		  if($lytxt1==$txt1){
			  $(this).val("");
			  }
		  
		  })
	  $lycon1.blur(function(){
		  var $lytxt1=$(this).val();
		  if($lytxt1==""){
			  $(this).val($txt1);
			  }
		  })
})
$(function(){
	var $lycon2=$(".zfb");
  var $txt2=$(".zfb").val();
      $lycon2.focus(function(){
		  var $lytxt2=$(this).val();
		  if($lytxt2==$txt2){
			  $(this).val("");
			  }
		  
		  })
	  $lycon2.blur(function(){
		  var $lytxt2=$(this).val();
		  if($lytxt2==""){
			  $(this).val($txt2);
			  }
		  })
})
$(function(){
	var $lycon3=$(".shuaiyiju");
  var $txt3=$(".shuaiyiju").val();
      $lycon3.focus(function(){
		  var $lytxt3=$(this).val();
		  if($lytxt3==$txt3){
			  $(this).val("");
			  }
		  
		  })
	  $lycon3.blur(function(){
		  var $lytxt3=$(this).val();
		  if($lytxt3==""){
			  $(this).val($txt3);
			  }
		  })
})



$(function(){
	var $sub4=$(".sub4");
	var $ly1=$(".lycon1").val();
	$sub4.click(function(){
		var $ly=$(".lycon1").val();
		if($ly==""||$ly==$ly1){
			return false;
			}else{
				return true;
				}
		})
	})
$(function(){
	var $sub2=$(".sub2");
	var $zsname=$(".zsname").val();
	var $zfb=$(".zfb").val();
	$sub2.click(function(){
		var $zs=$(".zsname").val();
		var $zf=$(".zfb").val();
		if($zs==""||$zf==""||$zs==$zsname||$zf==$zfb){

			return false;
			
			}else{
				return true;
				}
		})
	})
$(function(){
	var $sub3=$(".sub3");
	$sub3.click(function(){
		var $tx=$(".lycon").val();
		var $txlen=$(".lycon").val().length;
		if($tx==""||$txlen>120){

			return false;
			}else{
				return true;
				} 
		})
	})
$(function(){
	var $sub1=$(".sub1");
	$sub1.click(function(){
		var $syj1=$(".shuaiyiju").val();
		var $sylen=$(".shuaiyiju").val().length;
		if($syj1==""||$sylen>120){

			return false;
			}else{
				return true;
				} 
		})
	})
